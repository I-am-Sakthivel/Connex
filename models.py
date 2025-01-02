from extn import db,sec
from flask_security import UserMixin,RoleMixin
from flask_security.models import fsqla_v3 as fsq

fsq.FsModels.set_db_info(db)

class User(db.Model,UserMixin):
    # a simple relation with that has all the users in it. This will have id, name and role as those would be easy to identify
    #id is a string where first letter is either I,A or S denoting their role in this platform
    id=db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String(65), unique = True, nullable = False)
    roles = db.relationship('Role', secondary='user_roles')

class Role(db.Model,RoleMixin):
    id=db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80),nullable=False)

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class Influencer(db.Model):
    __tablename__='Influencer'
    email_id=db.Column(db.String, db.ForeignKey('user.email'),primary_key = True)
    category=db.Column(db.String(80),nullable=False)
    Niche=db.Column(db.String(80),nullable=False)
    Reach=db.Column(db.Integer,nullable=False)
    Balance=db.Column(db.Integer,nullable=False)
    Flag=db.Column(db.String(80),nullable=False,default='True')
    site=db.Column(db.String(80),nullable=False)

class Sponsor(db.Model):
    __tablename__='Sponsor'
    email_id=db.Column(db.String, db.ForeignKey('user.email'),primary_key = True)
    Industry=db.Column(db.String(80),nullable=False)
    Flag=db.Column(db.String(80),nullable=False,default='True')
    Approval=db.Column(db.String(80),nullable=False,default='False')
    site=db.Column(db.String(80),nullable=False)
class Campaigns(db.Model):
    __tablename__='Campaigns'
    C_id=db.Column(db.Integer, primary_key = True)
    s_email=db.Column(db.String,db.ForeignKey('Sponsor.email_id'))
    title=db.Column(db.String(80),nullable=False)
    Message=db.Column(db.String(80),nullable=False)
    S_date=db.Column(db.String(80),nullable=False)
    E_date=db.Column(db.String(80),nullable=False)
    Budget=db.Column(db.Integer,nullable=False)
    Niche=db.Column(db.String(80),nullable=False)
    Flag=db.Column(db.String(80),nullable=False,default='True')


class Ads(db.Model):
    __tablename__='Ads'
    A_id=db.Column(db.Integer, primary_key = True)
    C_id=db.Column(db.Integer, db.ForeignKey('Campaign.C_id'))
    I_email=db.Column(db.String,db.ForeignKey('Influencer.email_id'))
    title=db.Column(db.String(80),nullable=False)
    Message=db.Column(db.String(80),nullable=False)
    Flag=db.Column(db.String(80),nullable=False,default='True')
    Status=db.Column(db.String(80),nullable=False,default='Pending')
    salary=db.Column(db.Integer)
    Negotiated=db.Column(db.Integer,nullable=False)

class seen(db.Model):
    __tablename__='seen'
    pk=db.Column(db.Integer,primary_key=True)
    A_id=db.Column(db.Integer,db.ForeignKey('Ads.A_id'))
    b_date=db.Column(db.String(80),nullable=False)
    seen=db.Column(db.String(80),nullable=False,default='no')