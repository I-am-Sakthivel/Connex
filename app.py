from flask import Flask
from views import create_view
from extn import db,sec
from create_initial_data import create_data
from campaigns import api
from ads import adpi
from influencer import ipi
from sponsor import spi
from flask_caching import Cache
from worker import celery_init_app
from tasks import remaind
import flask_excel as excel
from celery import Celery
from celery.schedules import crontab
from mailing_function import mailing
celery_app=None
def create_app():
    app=Flask(__name__)
    cache=Cache(app)
    app.config['SECRET_KEY']="secret"
    app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///baknd.db"
    app.config['SECURITY_PASSWORD_SALT']='salt'
    db.init_app(app)
    with app.app_context():
        from models import User,Role
        from flask_security import SQLAlchemyUserDatastore
        ud=SQLAlchemyUserDatastore(db,User,Role)
        sec.init_app(app,ud)
        db.create_all()
        create_data(ud)
        celery_app=celery_init_app(app)
        
    app.config['WTF_CSRF_CHECK_DEFAULT']=False
    app.config["SECURITY_CSRF_PROTECH_MECHANISMS"]=[]
    app.config["SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS"]=True
    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
    app.config['SECURITY_TOKEN_MAX_AGE'] = 3600 #1hr
    app.config['SECURITY_LOGIN_WITHOUT_CONFIRMATION'] = True
    app.config['DEBUG']=True
    app.config['CACHE_TYPE']='RedisCache'
    app.config['CACHE_DEFAULT_TIMEOUT']=50
    app.config['CACHE_REDIS_HOST'] = 'localhost'
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_REDIS_DB'] = 0
    app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
    create_view(app,ud)
    api.init_app(app)
    adpi.init_app(app)
    ipi.init_app(app)
    spi.init_app(app)
    return app



if __name__=='__main__':
    app=create_app()
    app.run(debug=True)
    excel.init_excel(app)

c_b=Celery()
c_b.config_from_object("celeryconfig")
c_b.set_default()
@c_b.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #sending influencers email at 5:40 in the evening
    r_inf,r_spons=mailing()
    for i in r_inf:
        sender.add_periodic_task(crontab(hour=20, minute=2),remaind.s(i[0],'Your Daily Notification from Connex',i[1]))
    for i in r_spons:
        sender.add_periodic_task(crontab(hour=20, minute=8,day_of_month=1),remaind.s(i[0],'Your Daily Notification from Connex',i[1]))
    
