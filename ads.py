from flask_restful import Resource,Api,fields,reqparse,marshal_with
from flask import jsonify
from flask_security import auth_required
from models import Campaigns
from extn import db
from views import cur,conn,current_user
adpi=Api(prefix='/api')
parser=reqparse.RequestParser()


parser.add_argument('A_id', type=int)
parser.add_argument('C_id', type=int)
parser.add_argument('I_email', type=str)
parser.add_argument('title', type=str)
parser.add_argument('Title', type=str)
parser.add_argument('Message', type=str)
parser.add_argument('Flag', type=str)
parser.add_argument('Status', type=str)
parser.add_argument('salary', type=int)
parser.add_argument('Salary', type=int)
parser.add_argument('Negotiated', type=int)
parser.add_argument('bud', type=int)
parser.add_argument('cham', type=bool)
parser.add_argument('chat', type=bool)
parser.add_argument('t_date',type=str)
advert_fields={
    "A_id":fields.Integer,
    "C_id":fields.Integer,
    "I_email":fields.String,
    "title":fields.String,
    "Message":fields.String,
    "salary":fields.Integer,
    "Status":fields.String,
    "Flag":fields.String,
    "Negotiated":fields.Integer
}

def upd(A_id,field,val):
    q="update Ads set {field}='{val}' where A_id={aid}".format(field=field,val=val,aid=A_id)
    cur.execute(q)
    conn.commit()
def fn(l):
    data=[]
    for i in l:
        d={}
        d['A_id']=i[0]
        d['C_id']=i[1]
        d['I_email']=i[2]
        d['Title']=i[3]
        d['Message']=i[4]
        d['Flag']=i[5]
        d['Status']=i[6]
        d['Salary']=i[7]
        d['Negotiated']=i[8]
        data.append(d)
    return data

class ads(Resource):
    @auth_required('token')
    def get(self):
        role=current_user.roles[0].name
        if role=='Spons':
            q="select * from Ads where C_id in (select C_id from Campaigns where s_email='{}')".format(current_user.email)
            cur.execute(q)
            ads_of_sponsor=fn(cur.fetchall()) #all the ads of the sponsor
            return ads_of_sponsor,200
        elif role=='Inf':
            q="select * from Ads where I_email='{}' and Flag='True'".format(current_user.email)
            cur.execute(q)
            ads=cur.fetchall()#contains the ads the influencer has been a part of
            ads=fn(ads)
            #for ads shown to Influencer who are not part of 
            q='select * from Ads where C_id in (select C_id from Ads where I_email<>"{email}" and C_id in (select C_id from Campaigns where Niche="Public" or Niche in (select Niche from Influencer where I_email="{email}")))'.format(email=current_user.email)
            cur.execute(q)
            ads_Influ_not_partof=fn(cur.fetchall())
            return {"ads":ads,"ads_Influ_not_partof":ads_Influ_not_partof},200
        elif role=='Admin':
            q="select * from Ads"
            cur.execute(q)
            ads=cur.fetchall()
            flagged_ads,un_flagged_ads=[],[]
            for i in ads:
                if i[5]=='true':
                    un_flagged_ads.append(i)
                else:
                    flagged_ads.append(i)
            return {"flagged_ads":flagged_ads,"un_flagged_ads":un_flagged_ads},200 #Admin can see every advertisment 

    
    @auth_required('token')
    def post(self):
        args=parser.parse_args()
        q='insert into Ads(C_id,I_email,title,Message,Salary,Status,Negotiated) values({cid},"{I_email}","{title}","{message}",{salary},"{status}",{neg})'.format(cid=args.C_id,I_email=args.I_email,title=args.title,message=args.Message,salary=args.salary,neg=args.Negotiated,status=args.Status)
        cur.execute(q)
        conn.commit()
        q1='select A_id from Ads order by A_id Desc'
        cur.execute(q1)
        aid=cur.fetchone()[0]
        role=current_user.roles[0].name
        if role=='Spons':
            q2="insert into seen(A_id,b_date) values({aid},Date('now'))".format(aid=aid)
        elif role=='Inf':
            q2="insert into seen(A_id,b_date,seen) values({aid},Date('now'),'yes')".format(aid=aid)
        cur.execute(q2)
        conn.commit()
        return {"Message":"Ad Added"},200
    
    @auth_required('token')
    def delete(self):
        args=parser.parse_args()
        if (args.Salary!=0):
            #change the budget back and take away the influencer's salary
            q1="update Campaigns set Budget=Budget+{sal} where C_id={cid}".format(cid=args.C_id,sal=args.Salary)
            cur.execute(q1)
            conn.commit()
            q2="update Influencer set Balance=Balance-{sal} where email='{em}'".format(sal=args.Salary,em=args.I_email)
            cur.execute(q2)
            conn.commit()
        q="delete from Ads where A_id={}".format(args.A_id)
        print(q)
        cur.execute(q)
        conn.commit()
        return {"Message":"Ad deleted"},200
    
    @auth_required('token')
    def put(self):
        args=parser.parse_args()
        role=current_user.roles[0].name
        if role== 'Admin':
            #admin can possible only flag or unflag the campaign.
            q='update Ads set Flag="{flag}" where A_id={aid}'.format(aid=args.A_id,flag=args.Flag)
            cur.execute(q)
            conn.commit()
        elif role=='Inf':
            #influ can change Pending to either Negotiated or Paid and only one of them will be sent to the server
            upd(args.A_id,'Status',args.Status)
            upd(args.A_id,'Negotiated',args.Negotiated)
            if args.Status=='Paid':
                upd(args.A_id,'Salary',args.Salary)
                qp="update Campaigns set Budget=Budget-{neg} where C_id={cid}".format(cid=args.C_id,neg=args.Negotiated)
                cur.execute(qp)
                conn.commit()
                q2="update Influencer set Balance=Balance+{sal} where email='{em}'".format(em=args.I_email,sal=args.Salary)
                cur.execute(q2)
                conn.commit()
        elif role=='Spons':
            #sponsor can change the Status to Pending ,Negotiated(the negotiated salary) and the Salary(once the satus is Either Negotiated or paid)
            upd(args.A_id,'Status',args.Status)
            upd(args.A_id,'Negotiated',args.Negotiated)
            if (args.Salary)!=0:
                #print(args.salary)
                q="update Campaigns set Budget=Budget-{Salary} where C_id={cid}".format(Salary=args.Salary,cid=args.C_id) #budget of the campaign will change only if salary is fixed
                q2="update Influencer set Balance={sal} where email='{em}'".format(em=args.I_email,sal=args.Salary)
                upd(args.A_id,'Salary',args.Salary)
                cur.execute(q)
                conn.commit()
                cur.execute(q2)
                conn.commit()
            if(args.cham):
                q="update Ads set Message='{msg}' where A_id={aid}".format(aid=args.A_id,msg=args.Message)
                cur.execute(q)
                conn.commit()
            if(args.chat):
                q="update Ads set Title='{title}' where A_id={aid}".format(aid=args.A_id,title=args.Title)
                cur.execute(q)
                conn.commit()
        return {"Message":"Ad Updated"},200


adpi.add_resource(ads,'/ads')
