from views import conn,cur
def conv(l):
    r=[]
    for i in l:
        r.append(i[0])
    return r

def mailing():
    l_inf=[]
    q='select email from Influencer where Flag="True"'
    cur.execute(q)
    inf_emails=conv(cur.fetchall())
    res_inf=[] #list containing (email,no of notifications not seen)
    for em in inf_emails:
        q2="select count(seen) from seen where A_id in (select A_id from Ads where I_email='{}') and seen!='yes'".format(em)
        cur.execute(q2)
        n_s=cur.fetchone()[0]
        msg="<h1>You have "+ str(n_s) +" unseen requests</h1>"
        res_inf.append((em,msg))
    #for sponsors we send the data like the best campaign, no of ads done ,budget remaining overall
    q='select email_id from Sponsor where Flag="True" and Approval="True"'
    cur.execute(q)
    spons_emails=conv(cur.fetchall())
    res_spons=[]# list of tuple with (em,campaign with max budget this month,total ads made,total budget allocated,total money spent)
    for em in spons_emails:
        q1="select title from Campaigns where s_email='{em}' and Budget in (select max(Budget) from Campaigns where s_email='{em}' and Flag='True' and ( s_date > Date('now','start of month','-1 month')))".format(em=em)
        q2="select count(A_id) from Ads where C_id in (select C_id from Campaigns where s_email='{}' and Flag='True' and ( s_date > Date('now','start of month','-1 month')))".format(em)
        q3="select sum(Budget) from Campaigns where s_email='{}' and Flag='True' and ( s_date > Date('now','start of month','-1 month'))".format(em)
        q4="select sum(Salary) from Ads where C_id in (select C_id from Campaigns where (s_email='{}') and (Flag='True') and (s_date > Date('now','start of month','-1 month')))".format(em)
        cur.execute(q1)
        title=cur.fetchone()
        if title:
            title=title[0]
        else:
            title='None'
        cur.execute(q2)
        no_ads=cur.fetchone()[0]
        cur.execute(q3)
        tot_bud=cur.fetchone()[0]
        if tot_bud==None:
            tot_bud=0
        cur.execute(q4)
        tot_sal=cur.fetchone()[0]
        if tot_sal==None:
            tot_sal=0
        mess="<h1> last month your most expensive campaign was '"+title+"', You have made "+str(no_ads)+" ads this month."+" you have allocated Rs."+str(tot_bud)+" this month. You have spent Rs."+str(tot_sal)+" this month </h1>"
        res_spons.append((em,mess))
    return res_inf,res_spons
mailing()