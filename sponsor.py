from flask_restful import Resource,Api,fields,reqparse,marshal_with
from flask_security import auth_required
from extn import db
from views import cur,conn,current_user
from flask import jsonify
spi=Api(prefix='/api')
parser=reqparse.RequestParser()
parser.add_argument("name",type=str)
parser.add_argument("email",type=str)
parser.add_argument('Industry',type=str)
parser.add_argument('Flag',type=str)
parser.add_argument('Approval',type=str)
parser.add_argument('site',type=str)
spons_fields={
    "email":fields.String,
    "Industry":fields.String,
    "Flag":fields.String,
    "Approval":fields.String,
    "site":fields.String
}

class Sponsor(Resource):
    @auth_required('token')
    def get(self):
        role=current_user.roles[0].name
        if role=='Spons':
            email=current_user.email
            q='select name,s.email_id,Industry,Flag,Approval,Site from Sponsor s,user u where s.email_id=u.email and u.email="{}"'.format(email)
            cur.execute(q)
            i=cur.fetchone()
            l=[]
            d={}
            d['name']=i[0]
            d['email']=i[1]
            d['ind']=i[2]
            d['flag']=i[3]
            d['approval']=i[4]
            d['site']=i[5]
            l.append(d)
            return l
        elif role=='Admin':
            #admin can see every sponsor's every detail
            q='select name,s.email_id,Industry,Flag,Approval,Site from Sponsor s,user u where s.email_id=u.email'
            cur.execute(q)
            data=cur.fetchall()
            l=[]
            for i in data:
                d={}
                d['name']=i[0]
                d['email']=i[1]
                d['ind']=i[2]
                '''if i[3]=='False' or i[3]=='false':
                    d['flag']='false'
                elif  i[3]=='True' or i[3]=='true':
                    d['flag']='true'
                if i[4]=='False' or i[4]=='false':
                    d['Approval']='false'
                elif  i[4]=='True' or i[4]=='true':
                    d['Approval']='true' '''
                d['flag']=i[3]
                d['Approval']=i[4]
                d['site']=i[5]
                l.append(d)
            return l
        elif role=='Inf':
            #Influencers can see sponsors who have sponsored them past and present
            #they can also look into other sponsors who have had a good run with their friends (will do this as an optional feature)
            email=current_user.email
            q="select name,s.email_id,Industry,Flag,Approval,site from Sponsor s,user u where s.email_id=u.email and u.email in (select s_email from Campaigns where C_id in (select C_id from Ads where I_email='{}'))".format(email)
            cur.execute(q)
            data=cur.fetchall()
            #they can also see their sites
            q="select s.email_id,name,site from Sponsor s,user u where s.email_id=u.email"
            cur.execute(q)
            new_data=cur.fetchall()
            l=[]
            for k in new_data:
                d={}
                d['email']=k[0]
                d['name']=k[1]
                d['site']=k[2]
                l.append(d)
            return {"data":data,"sitedata":l}
    
    @auth_required('token')
    def put(self):
        args=parser.parse_args()
        #A sponsor can change all their details except flag and approval
        #Admin can only change flag and approval
        email=args['email']
        role=current_user.roles[0].name
        if role=='Spons':
            #to update email 
            q1="update user set email='{email}' where email='{cur_email}'".format(email=args['email'],cur_email=current_user.email)
            q2="update Sponsor set email_id='{email}' where email_id='{cur_email}'".format(email=args['email'],cur_email=current_user.email)
            cur.execute(q1)
            conn.commit()
            cur.execute(q2)
            conn.commit()
            #to update name
            q="update user set name='{name}' where email='{email}'".format(name=args['name'],email=args['email'])
            cur.execute(q)
            conn.commit()
            #to update Industry and site
            q1="update Sponsor set Industry='{ind}' where email_id='{email}'".format(ind=args['Industry'],email=args['email'])
            q2="update Sponsor set site='{site}' where email_id='{email}'".format(site=args['site'],email=args['email'])
            cur.execute(q1)
            conn.commit()
            cur.execute(q2)
            conn.commit()
            return {"message":"updated flag and stuff succesfully"}
        if role=='Admin':
            q="update user set active=1 where email='{}'".format(email)
            q2="update Sponsor set Approval='True' where email_id='{email}'".format(app=args['Approval'],email=args['email'])
            q3="update Sponsor set Flag='{flag}' where email_id='{email}'".format(flag=args['Flag'],email=args['email'])
            if (args['Approval']):
                cur.execute(q)
                conn.commit()
            cur.execute(q2)
            conn.commit()
            if args['Flag']:
                cur.execute(q3)
                conn.commit()
                print(q3)
            return {"message":"updated flag and stuff succesfully"}
        return '200'

spi.add_resource(Sponsor,'/spons')