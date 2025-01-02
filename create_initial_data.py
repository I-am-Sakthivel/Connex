from flask_security import SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from extn import db
def create_data(ud:SQLAlchemyUserDatastore):
    ## Creating Data ##
    ud.find_or_create_role(name='Admin')
    ud.find_or_create_role(name='Inf')
    ud.find_or_create_role(name='Spons')
    if not ud.find_user(email='admin@connex.in'):
        ud.create_user(name='Megha',email='admin@connex.in',password=hash_password('secret'),roles=['Admin'],active=True)
    if not ud.find_user(email='spons@comp1.in'):
        ud.create_user(name='Comp1',email='spons@comp1.in',password=hash_password('secret'),roles=['Spons'],active=True)
    if not ud.find_user(email='sakthi@gmail.com'):
        ud.create_user(name='Sakthi',email='sakthi@gmail.com',password=hash_password('secret'),roles=['Inf'],active=True)
    db.session.commit()