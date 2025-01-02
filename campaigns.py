from flask_restful import Resource,Api,fields,reqparse,marshal_with
from flask_security import auth_required
from models import Campaigns
from extn import db
from views import cur,conn,current_user
api=Api(prefix='/api')

parser=reqparse.RequestParser()
parser.add_argument('C_id', type=int)
parser.add_argument('s_email', type=str)
parser.add_argument('title', type=str)
parser.add_argument('Message', type=str)
parser.add_argument('S_date', type=str)
parser.add_argument('E_date', type=str)
parser.add_argument('Budget', type=int)
parser.add_argument('Niche', type=str)
parser.add_argument('Flag', type=str)
parser.add_argument('c_id',type=int)

campaign_fields={
    "C_id":fields.Integer,
    "s_email":fields.String,
    "title":fields.String,
    "Message":fields.String,
    "S_date":fields.String,
    "E_date":fields.String,
    "Budget":fields.Integer,
    "Niche":fields.String,
    "Flag":fields.String
}

def upd(C_id,field,val):
    q='update Campaigns set {field}="{val}" where C_id={cid}'.format(field=field,val=val,cid=C_id)
    cur.execute(q)
    conn.commit()

def conv(data):
    #this is a function that takes in a list we got from cur.fetchall() and returns a list of dictionaries as it is easier to acces in js
    l=[]
    for i in data:
        d={}
        d['c_id']=i[0]
        d['s_email']=i[1]
        d['title']=i[2]
        d['message']=i[3]
        d['s_date']=i[4]
        d['e_date']=i[5]
        d['budget']=i[6]
        d['niche']=i[7]
        d['flag']=i[8]
        if len(i)>9:
            d['site']=i[9]
            d['name']=i[10]
        l.append(d)
    return l

class Campaigns(Resource):
    @auth_required('token')
    def get(self):
        role=current_user.roles[0].name
        if role=='Spons':
            q='select * from Campaigns where s_email="{}"'.format(current_user.email)
            cur.execute(q)
            all_data=cur.fetchall()
            l=conv(all_data)
            return l
        if role=='Inf':
            q='select C_id,s_email,Title,Message,S_date,E_date,Budget,c.Niche,c.Flag,s.site,u.name from Campaigns c, Sponsor s,user u where (c.s_email=s.email_id and s.email_id=u.email) and ((Niche="public" or Niche in (select Niche from Influencer where email="{email}")) and (C_id not in (select C_id from Ads where I_email="{email}")))'.format(email=current_user.email)
            #Influencers can see all campaigns they are eligible for but not part of
            cur.execute(q)
            Influ_not_partof=cur.fetchall()
            Influ_not_partof=conv(Influ_not_partof)
            #The campaigns they are part of
            q="select C_id,s_email,Title,Message,S_date,E_date,Budget,c.Niche,c.Flag,s.site,u.name from Campaigns c, Sponsor s,user u where (c.s_email=s.email_id and s.email_id=u.email) and (C_id in (select C_id from Ads where I_email='{}' and Status='Paid'))".format(current_user.email)
            cur.execute(q)
            Influ_partof=cur.fetchall()
            Influ_partof=conv(Influ_partof)
            return{"partof":Influ_partof,"notpartof":Influ_not_partof},200
        elif role=='Admin':
            q="select C_id,s_email,Title,Message,S_date,E_date,Budget,c.Niche,c.Flag,s.site,u.name from Campaigns c, Sponsor s,user u where (c.s_email=s.email_id and s.email_id=u.email)"
            cur.execute(q)
            all_data=conv(cur.fetchall())
            return all_data
            
    
    @auth_required('token')
    def post(self):
        args=parser.parse_args()
        q='insert into Campaigns(s_email,title,Message,S_date,E_date,Budget,Niche) values("{s_email}","{title}","{Message}","{S_date}","{E_date}",{Budget},"{Niche}")'.format(C_id=args.C_id,s_email=args.s_email,title=args.title,Message=args.Message,S_date=args.S_date,E_date=args.E_date,Budget=args.Budget,Niche=args.Niche,Flag=args.Flag)
        print(q)
        cur.execute(q)
        conn.commit()
        return {"message":"campaign_created"},200
    
    @auth_required('token')
    def put(self):
        #two types of updating
        args=parser.parse_args()
        role=current_user.roles[0].name
        C_id=args.C_id
        if role=='Admin':
            #admin can possible only flag or unflag the campaign.
            q="update Campaigns set Flag='{flag}' where C_id={cid} ".format(flag=args.Flag,cid=args.C_id)
            cur.execute(q)
            conn.commit()
        else:
            for arg in campaign_fields:
                if arg!='C_id' and args[arg]:
                    if type(args[arg])==int:
                        q="update Campaigns set Budget='{budget}' where C_id={cid} ".format(budget=args[arg],cid=args.C_id)
                        cur.execute(q)
                        conn.commit()
                    else:
                        upd(C_id,arg,args[arg])
        return {"message":"campaign_updated"},200
    
    @auth_required('token')
    def delete(self):
        args=parser.parse_args()
        q='delete from Campaigns where C_id={}'.format(args.c_id)
        cur.execute(q)
        conn.commit()
        return {"message":"campaign_deleted"},200

api.add_resource(Campaigns,'/camps')