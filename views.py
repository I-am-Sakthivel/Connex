from flask import render_template,jsonify,request,send_file
from flask_security.utils import hash_password
from flask_security import login_required,roles_required,auth_required,current_user,roles_accepted,SQLAlchemyUserDatastore    
import sqlite3
from extn import db
from tasks import csv
from celery.result import AsyncResult
conn=sqlite3.connect(r'instance/baknd.db',check_same_thread=False)
cur=conn.cursor()

def cor(l):
    r=[]
    for i in l:
        r.append(i[0])
    return r

def conv(data,r):
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
        if i[0] in r:
             d['part']='true'
        else:
             d['part']='false'
        l.append(d)
    return l    

def inc(l):
     #u.name,i.email,Category,Niche,Reach,Flag,site
    r=[]
    for i in l:
        d={}
        d['name']=i[0]
        d['email']=i[1]
        d['category']=i[2]
        d['niche']=i[3]
        d['reach']=i[4]
        d['flag']=i[5]
        d['site']=i[6]
        r.append(d)
    return r

def create_view(app,ud:SQLAlchemyUserDatastore):
    @app.route('/')
    def home():
        return render_template('index.html')
    @app.route('/register',methods=['POST'])
    def register():
        data=request.json
        name=data['name']
        email=data['email']
        passwd=data['password']
        role=data['role']
        if role=='Inf':
            cat=data['Cat']
            nic=data['Nic']
            reach=int(data['reach'])
            site=data['site']
            act=True
            q="insert into Influencer(email,Category,Niche,Reach,Balance,site) values('{email}','{cat}','{nic}',{reach},0,'{site}')".format(email=email,cat=cat,nic=nic,reach=reach,site=site)
            cur.execute(q)
            conn.commit()
        if role=='Spons':
            ind=data['Ind']
            site=data['site']
            act=False
            q="insert into Sponsor(email_id,Industry,site) values('{email}','{ind}','{site}')".format(email=email,ind=ind,site=site)
            cur.execute(q)
            conn.commit()
        if (email and passwd) and role:
            if not ud.find_user(email=email):
                    ud.create_user(name=name,email=email,password=hash_password(passwd),roles=[role],active=act)
                    db.session.commit()
            else:
                 return (jsonify({"message":"User_exists"}),200)
        else:
            return (jsonify({"message":"Invalid"}),401)
        return ('success',200)
    
    @app.route('/profile')
    @login_required
    def profile():
         email=current_user.email
         name=current_user.name
         role=current_user.roles[0].name
         token=current_user.get_auth_token()
         if role=='Inf':
              q="select Category,Niche,Reach,Balance,flag,site from Influencer where email='{}'".format(email)
              cur.execute(q)
              cat,nic,reach,bal,flag,site=cur.fetchone()
              q2="select * from Campaigns where Niche in ('Public','{}')".format(nic)
              cur.execute(q2)
              camp=cur.fetchall()
              return jsonify({"email":email,"name":name,"cat":cat,"nic":nic,"reach":reach,"bal":bal,"flag":flag,"site":site,"role":role,"camps":camp,"token":token}),200
         elif role=='Spons':
              q="select Industry,Flag,site from Sponsor where email_id='{}'".format(email)
              cur.execute(q)
              ind,flag,site=cur.fetchone()
              return jsonify({"email":email,"name":name,"role":role,"ind":ind,"flag":flag,"site":site,"token":token}),200
         else:
              q="select * from Campaigns"
              cur.execute(q)
              camp=cur.fetchall()
              q="select * from Ads"
              cur.execute(q)
              ads=cur.fetchall()
              q='select * from Sponsor'
              cur.execute(q)
              spons=cur.fetchall()
              q="select * from Influencer"
              cur.execute(q)
              inf=cur.fetchall()
              q='select name from user where email="{}"'.format(current_user.email)
              cur.execute(q)
              name=cur.fetchone()[0]
              return jsonify({"text":"under construction. Admin's db should show some stats","name":name,"role":'Admin',"camps":camp,"Ads":ads,"spons":spons,"inf":inf,"token":token}),200
    @app.route('/inf/spons/<cid>',methods=['POST','GET'])
    @roles_required('Spons')
    @auth_required('token')
    def inf_spons(cid):
        q1="select Niche from Campaigns where C_id={}".format(cid)
        cur.execute(q1)
        Nic=cur.fetchone()[0]
        if Nic=='public':
            q="select name,u.email from user u,Influencer i where i.email=u.email and Flag='True'"
        else:
            q="select name,u.email from user u,Influencer i where i.email=u.email and (Flag='True' and Niche ='{}')".format(Nic)
        cur.execute(q)
        dt=cur.fetchall()
        l=[]
        for i in dt:
             d={}
             d['name']=i[0]
             d['email']=i[1]
             l.append(d)
        return l,'200'
    @app.route('/aretheyloggedin')
    def logged_in():
         if current_user.is_authenticated:
              return jsonify({"message":"yes"})
         else:
              return jsonify({"message":"no"})
    @app.route('/search')
    @auth_required('token')
    def search():
         role=current_user.roles[0].name
         em=current_user.email
         if role=='Inf':
              #Influencer can search for all eligible campaigns that are running 
              q_nic="select Niche from Influencer where email='{}'".format(em)
              cur.execute(q_nic)
              nic=cur.fetchone()[0]
              q="select C_id,c.s_email,Title,Message,S_date,E_date,Budget,Niche,c.Flag,s.site,u.name from Campaigns c, Sponsor s,user u  where ((c.s_email=u.email and u.email=s.email_id) and (Niche='{}' or Niche='public')) and (c.Flag='True')".format(nic)
              cur.execute(q)
              l=cur.fetchall()
              #Let's add another attribute specifying if the influencer is already part of the campaign
              q_cid="select C_id from Ads where I_email='{}'".format(em)
              cur.execute(q_cid)
              cid=cor(cur.fetchall())
              res=conv(l,cid)
              return {"res":res,"role":role,"email":em},'200'
         elif role=='Spons':
              #let the frontend filter it,here they can get only the details
              q="select u.name,i.email,Category,Niche,Reach,Flag,site from user u,Influencer i where (u.email=i.email) and (Flag='True')"
              cur.execute(q)
              data=inc(cur.fetchall())
              return {"res":data,"role":role,"email":em},'200'
    
    @app.route('/turntoseen')
    @auth_required('token')
    @roles_required('Inf')
    def seen():
         #this will just update all those ads as seen (to 'yes') once the requests tab is mounted
         em=current_user.email
         q="update seen set seen='yes' where A_id in (select A_id from Ads where I_email='{}')".format(em)
         cur.execute(q)
         conn.commit()
         return '200'
    @app.route('/stats')
    @auth_required('token')
    def stats():
         #this will return the stats for each person with respect to their role
        role=current_user.roles[0].name
        em=current_user.email
        if role=='Inf':
             #Descriptive stats of their previous salaries
            q="select Salary from Ads where I_email='{}'".format(em)
            cur.execute(q)
            sal=cor(cur.fetchall())
            #mean=sum(sal)/len(sal)
            mean=sum(sal)/len(sal)
            sorted_sal=sorted(sal)
            n=len(sal)
            if n%2==0:
                median=(sorted_sal[n//2]+sorted_sal[(n//2) +1])/2
            else:
                 median=sorted_sal[(n+1)//2]            
            max_sal=sorted_sal[-1]
            #give out a frequency table
            d={}
            for i in sorted_sal:
                if i in d:
                    d[i]+=1
                else:
                    d[i]=1
            q2="select name from user where email in (select s_email from Campaigns where C_id in (select C_id from Ads where I_email='{}' group by I_email order by count(A_id) desc))".format(em)
            cur.execute(q2)
            spons_name=cor(cur.fetchall())
            #spons_name has the sponsors arranged from more colabs to least
            q3="select sum(salary) from Ads where (A_id in (select A_id from seen where b_date between date('now','start of month','-1 month') and date('now'))) and I_email='{}'".format(em)
            cur.execute(q3)
            one_month_sal=cur.fetchone()[0]
            return {"role":role,"mean":mean,"median":median,"max_sal":max_sal,"feq_dist":d,"spons_name":spons_name},200
        elif role=='Spons':
            #sponsor sees the most participated campaign, most spent campaign, frequent collaborating Influencer
            q="select title from Campaigns where (C_id in (select C_id from Ads group by C_id order by count(C_id) desc)) and (s_email='{}')".format(em)
            cur.execute(q)
            camp=cor(cur.fetchall()) #has a list of camapigns in descending order of number of participants
            q2="select title from Campaigns where (s_email='{}') and (C_id in (select C_id from Ads group by C_id order by sum(Salary) desc))".format(em)
            cur.execute(q2)
            msp=cor(cur.fetchall()) #most spent campaigns in descending order
            q3="select name from user where email in (select I_email from Ads where C_id in (select C_id from Campaigns where s_email='{}') group by I_email order by count(A_id) desc )".format(em)
            cur.execute(q3)
            names=cor(cur.fetchall())#collaborating influencer in descending order of no. of colabs
            return {"role":role,"camp":camp,"msp":msp,"names":names},200
        else:
            #Admin can see the best performing Influencer and campaign in terms of money and no.of ads done 
            q1="select name from user where email in (select I_email from Ads group by I_email order by count(A_id) desc)"
            cur.execute(q1)
            inf_n=cor(cur.fetchall())#in terms of no.of ads
            q2="select name from user where email in (select I_email from Ads group by I_email order by sum(Salary) desc)"
            cur.execute(q2)
            inf_s=cor(cur.fetchall())#in terms of salary
            q3="select title from Campaigns where C_id in (select C_id from Ads group by C_id order by count(A_id) desc)"
            cur.execute(q3)
            cp_n=cor(cur.fetchall())#most participated campaigns
            q4="select title from Campaigns where C_id in (select C_id from Ads group by C_id order by sum(Salary) desc)"
            cur.execute(q4)
            cp_s=cor(cur.fetchall())#in terms of money spent
            q5="select name from user where email in (select s_email from Campaigns where budget in (select max(budget) from Campaigns))"
            cur.execute(q5)
            sp_max_budget=cor(cur.fetchall())#sponsor who gave the maximum budget
            return {"role":role,"inf_n":inf_n,"inf_s":inf_s,"cp_n":cp_n,"cp_s":cp_s,"sp_max_budget":sp_max_budget},200          
        return '200'

    @app.route('/csv')
    def csv_out():
        em=current_user.email
        res= csv.delay(em)
        return {"task_id":res.id},200
    @app.route('/fetc/<id>')
    def fet_csv(id):
        res=AsyncResult(id)
        if res.ready():
            return send_file(res.result)
    @app.route('/mail')
    def mail_user():
        #this will mail user thier necessites.
        
        return '200'