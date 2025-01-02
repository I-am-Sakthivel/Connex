from flask_restful import Resource,Api,fields,reqparse,marshal_with
from flask_security import auth_required
from extn import db
from views import cur,conn,current_user
from flask import jsonify
ipi=Api(prefix='/api')
parser=reqparse.RequestParser()
parser.add_argument("email",type=str)
parser.add_argument("category",type=str)
parser.add_argument("Niche",type=str)
parser.add_argument("Reach",type=int)
parser.add_argument("Balance",type=int)
parser.add_argument("Flag",type=str)
parser.add_argument("site",type=str)
parser.add_argument("name",type=str)
parser.add_argument('at',type=str)
inf_fields={
    "name":fields.String,
    "email":fields.String,
    "category":fields.String,
    "Niche":fields.String,
    "Reach":fields.Integer,
    "Balance":fields.Integer,
    "Flag":fields.String,
    "site":fields.String
}

class Influencer(Resource):
    @auth_required('token')
    def get(self):
        role=current_user.roles[0].name
        #what does each user need?
        #Influencer needs to see theirs data and their friends data, deal with it afterwards
        if role=='Inf':
            email=current_user.email
            name=current_user.name
            q='select * from Influencer where email="{}"'.format(email)
            cur.execute(q)
            info=cur.fetchone()
            cat=info[1]
            nic=info[2]
            reach=info[3]
            bal=info[4]
            flag=info[5]
            site=info[6]
            inf_data=jsonify({"email":email,"category":cat,"Niche":nic,"Reach":reach,"Balance":bal,"Flag":flag,"site":site,"name":name,"role":role})
            return inf_data
        elif role=='Admin':
            q1='select name,i.email,Category,Niche,Reach,Balance,Flag,site from user u,Influencer i where (i.email=u.email)'
            cur.execute(q1)
            info=cur.fetchall()
            res=[]
            for i in info:
                d={}
                d['name']=i[0]
                d['email']=i[1]
                d['category']=i[2]
                d['niche']=i[3]
                d['reach']=i[4]
                d['balance']=i[5]
                d['flag']=i[6]
                d['site']=i[7]
                res.append(d)
            return res,'200'
    @auth_required('token')
    def put(self):
        role=current_user.roles[0].name
        if role=='Inf':
            #Influencer can edit their email,name,category,reach,site,Niche
            #they can't edit their balance and flag
            email=current_user.email    
            args=parser.parse_args()
            at=args.at
            match at:
                case 'name':
                    q='update user set name="{name}" where email="{em}"'.format(name=args.name,em=email)
                case 'niche':
                    q='update Influencer set Niche="{nic}" where email="{em}"'.format(nic=args.Niche,em=email)
                case 'cat':
                    q='update Influencer set Category="{cat}" where email="{em}"'.format(cat=args.category,em=email)
                case 'rea':
                    q='update Influencer set Reach={rea} where email="{em}"'.format(rea=args.Reach,em=email)
            cur.execute(q)
            conn.commit()
            return {"Message":"Updated Succesfully"},'200'
        elif role=='Admin':
            #Admin can flag or unflag an Influencer
            d={"True":"False","False":"True"} #this dictionary will be used so that admin can flip the flag of the influencer
            args=parser.parse_args()
            flag=args['Flag']
            email=args['email']
            q="update Influencer set Flag='{f}' where email='{e}'".format(f=flag,e=email)#This only flags the user, the can still login to the app
            cur.execute(q)
            conn.commit()
            return {"Message":"Updated Succesfully"},'200'

ipi.add_resource(Influencer,'/inf')