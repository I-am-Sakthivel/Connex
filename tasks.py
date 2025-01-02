from celery import shared_task
import csv
from csv import DictWriter
from models import Campaigns
from flask_excel import make_response_from_query_sets as mrs,make_response_from_array as mra,make_response_from_records as mrr
import sqlite3
from mail import send_email
conn=sqlite3.connect("instance/baknd.db",check_same_thread=False)
cur=conn.cursor()

def conv(l):
    r=[]
    for i in l:
        d={}
        d['title']=i[0]
        d['message']=i[1]
        d['s_date']=i[2]
        d['e_date']=i[3]
        d['budget']=i[4]
        d['niche']=i[5]
        r.append(d)
    return r


@shared_task()
def add(x,y):
    return x+y

@shared_task(ignore_result=False)
def mul(x,y):
    return x*y

@shared_task(ignore_result=False)
def csv(em):
    #create a csv file that is the table for each sponsor where the argument is their email
    q="select Title,Message,S_date,E_date,Budget,Niche from Campaigns where s_email='{}'".format(em)
    cur.execute(q)
    res=conv(cur.fetchall())
    fname='./user-downloads/camps_'+em+'.csv'
    with open(fname, 'w', newline='') as csvfile:
        fieldnames = ['title','message','s_date','e_date','budget','niche']
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(res)
    return fname

@shared_task(ignore_result=True)
def remaind(user_email,title,text):
    send_email(user_email,title,text)
    return '200'