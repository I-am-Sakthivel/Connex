import router from "../utils/router.js"
import crecam from "../components/cre_cam.js"

function inval_date(st){
    !isNaN(new Date(st))
}

const spons_profile={
    template:`<div v-if="approval=='True'">
    <div v-if="flag=='True'">
    
    <h1> Welcome {{name}} </h1>
    <router-link to='/search'><button class='btn btn-link' >Search for Influencers </button></router-link>
    <table class='table-primary table-bordered'>

    <button class='btn btn-danger' @click='exp()'> Export as a csv </button>
    <caption class="caption">Active Campaigns</caption>
    <tr>
        <th scope="col">C_id</th>
        <th scope="col">title</th>
        <th scope="col">Message</th>
        <th scope="col">S_date</th>
        <th scope="col">E_date</th>
        <th scope="col">Budget</th>
        <th scope="col">Niche</th>
        </tr>
        <tr v-for="c in camps" v-if="new Date(c.e_date) >= date"> 
            <td>{{c.c_id}}</td>
            <td>{{c.title}}</td>
            <td>{{c.message}}</td>
            <td>{{c.s_date}}</td>
            <td>{{c.e_date}}</td>
            <td>{{c.budget}}</td>
            <td>{{c.niche}}</td>
            <td>
            <div>
            <button class='btn btn-info' @click='upd(c)'>Update</button>
            <button class='btn btn-danger' @click='del(c)'>Delete</button>
            <button class='btn btn-warning' @click='cread(c)'>Create Advert </button>
            </div>
            </td>
        </tr>
</table>

<table class='table-danger table-bordered' v-if="ads.length >0">
    <tr>
        <th>Influencer</th>
        <th>Title</th>
        <th>Message</th>
        <th>Negotiated pay</th>
        <th>              </th>
    </tr>
    <tr v-for="ad in ads" v-if="ad.Flag=='True'">
        <td> {{ad.I_email}}</td>
        <td> {{ad.Title}} </td>
        <td> {{ad.Message}} </td>
        <td> {{ad.Negotiated}}  </td>
        <div>
        <button class='btn btn-info' @click='upad(ad)' v-if="ad.Status=='Negotiated'">Update</button>
        <button class='btn btn-success' @click='acc(ad)' v-if="ad.Status=='Negotiated'">Accept</button>
            <button class='btn btn-danger' @click='delad(ad)' >Reject</button>
            <button class='btn btn-warning' @click='cham(ad)'>Change Message</button>
            <button class='btn btn-info' @click='chat(ad)'>Change Title</button>
        </div>
    </tr>
</table>
<div v-if="create" >
<button class='btn-danger' @click='cre_cam'>Not now</button>
</div>
<div v-if="cred">
<table>
    <tr>
        <th>Select your Influencer</th>
        <th>Title of the advertisment</th>
        <th>Message to the Influencer</th>
        <th>Name your Price</th>
        <th>               </th>
    </tr>
    <tr>
        <td>
            <select v-model="new_ad.I_email" text="Influencer" placeholder="Select your Influencer"  v-for ="val in this.inf_lst">
                <option :value=val.email>{{val.name}}</option>
              </select>
        </td>
        <td> <input type="text" placeholder='Enter your title' v-model='new_ad.title' required> </td>
        <td> <input type="text" placeholder='Enter your Message' v-model='new_ad.Message' required> </td>
        <td> <input type="number" v-model='new_ad.Negotiated' required> </td>
        <td> <button class='btn btn-success' @click='create_ad'>Create request </button></td>
    </tr>
</table>
</div>
<div v-else>
<button class='btn-success' @click='cre_cam'>Create new Campaign</button>
</div>
<div v-if="create">
<table>
    <tr>
        <th scope="col">title</th>
        <th scope="col">Message</th>
        <th scope="col">S_date</th>
        <th scope="col">E_date</th>
        <th scope="col">Budget</th>
        <th scope="col">Niche</th>
        <th scope="col">       </th>
        </tr>
        <tr>
        <td> <input type="text" placeholder='Enter your title' v-model='new_camp.title' required> </td>
        <td> <input type="text" placeholder='Explain your campaign' v-model="new_camp.Message" required></td>
        <td> <input type="date" v-model="new_camp.S_date" required> </td>
        <td> <input type="date" v-model="new_camp.E_date" required> </td>
        <td> <input type="number" v-model="new_camp.Budget" required> </td>
        <td> <input type="text" placeholder='Enter your niche' v-model="new_camp.Niche" required> </td>
        </tr>
</table>
<p v-if="new_camp.Niche.length > 1">
You are creating a new campaign called {{new_camp.title}} starting on {{new_camp.S_date}} and ending on {{new_camp.E_date}} with a budget of &#8377{{new_camp.Budget}}
<button class='btn-info' @click='cre'> Yes Create </button>
</p>

</div>
    </div>
    <div v-if='flag=="False"'>
    <p>You are flagged!!</p>
    </div>
    </div>
    <div v-else>
    <p>You are not approved </p>
    </div>`,
data(){
    return {
        name:'',
        ind:'',
        email:'',
        flag:'',
        approval:'',
        site:'',
        camps:[],
        ads:[],
        url:window.location.origin,
        date:new Date() ,
        create:false,
        new_camp:{
            title:'',
            Message:'',
            S_date:new Date(),
            E_date:new Date(),
            Budget:0,
            Niche:'',
            Flag:'True',
            s_email:''
        },
        new_ad:{
            C_id:0, 
            I_email:'',
            title:'',
            Message:'',
            salary:0,
            Status:'Pending',
            Negotiated:0,
        },
        cred:false,
        inf_lst:[],
        bud:0,
        c_temp:{},
    }
},
methods:{
    cre_cam(){
        this.create=!this.create
    },
    async cread(c){
        this.cred=!this.cred
        this.new_ad.C_id=c.c_id
        this.bud=c.budget
        const url=window.location.origin
        let ul='/inf/spons/'+c.c_id
        const val_inf=await fetch(url + ul,{
            headers: {
              "Authentication-Token": sessionStorage.getItem("token"),
            },
          })
        if (val_inf.ok){
            let inf=await val_inf.json()
            this.inf_lst=inf
        }
        this.c_temp=c
    },
    async create_ad(){
        if (this.new_ad.Negotiated > this.bud){
            window.alert("Your Price is higher than your campaign's budget. Change any of those")
            this.new_ad.Negotiated=0
        }
        else{
        this.c_temp.Budget=this.c_temp.budget
        this.c_temp.C_id=this.c_temp.c_id
        this.c_temp.Message=this.c_temp.message
        this.c_temp.S_date=this.c_temp.s_date
        this.c_temp.E_date=this.c_temp.e_date
        this.c_temp.Niche=this.c_temp.niche
        this.c_temp.Flag=this.c_temp.flag    
        const url=window.location.origin
        const val= await fetch(
            url+'/api/ads',
            {
                method:'POST',
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": sessionStorage.getItem("token")
                  },
                  body: JSON.stringify(this.new_ad)
            })
            const put_req=await fetch(
                this.url+'/api/camps',
                {
                    method:'PUT',
                    headers: {
                        "Content-Type": "application/json",
                        "Authentication-Token": sessionStorage.getItem("token")
                      },
                      body: JSON.stringify(this.c_temp)
                }
            )
            this.cred=!this.cred
            this.ads.push(this.new_ad)
    }},
    async cre(){
        this.new_camp.s_email=this.email
        const url=window.location.origin
        const val= await fetch(
            url+'/api/camps',
            {
                method:'POST',
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": sessionStorage.getItem("token")
                  },
                  body: JSON.stringify(this.new_camp)
            })
        if (val.ok){
            let info = await val.json()
        }
        window
    },
    async del(c){
      const ind=this.camps.indexOf(c)
      if(confirm("Are you sure ?")){
       const del_req=fetch(
        this.url+'/api/camps',
        {
            method:'DELETE',
            headers: {
                "Content-Type": "application/json",
                "Authentication-Token": sessionStorage.getItem("token")
              },
              body: JSON.stringify(this.camps[ind])
        })
        this.camps.splice(ind,1)
      }
    },
    async delad(ad){
        const ind=this.ads.indexOf(ad)
        if(confirm("Are you sure ?")){
            const del_req=fetch(
             this.url+'/api/ads',
             {
                 method:'DELETE',
                 headers: {
                     "Content-Type": "application/json",
                     "Authentication-Token": sessionStorage.getItem("token")
                   },
                   body: JSON.stringify(this.ads[ind])
             })
             this.ads.splice(ind,1)
           }
    },
    async cham(ad){
        ad['cham']=true
        ad.Message=window.prompt('Are you changing your message from '+ad['Message']+' ?',ad['Message'])
        const put_req=await fetch(this.url+'/api/ads',{method:'PUT',headers: {"Content-Type": "application/json","Authentication-Token": sessionStorage.getItem("token")},body: JSON.stringify(ad)})
    },
    async chat(ad){
        ad['chat']=true
        ad.Title=window.prompt('Are you changing your title from '+ad['Title']+' ? ', ad['Title'])
        const put_req=await fetch(this.url+'/api/ads',{method:'PUT',headers: {"Content-Type": "application/json","Authentication-Token": sessionStorage.getItem("token")},body: JSON.stringify(ad)})
    },
    async upd(c){
        let op={}
        op['C_id']=c.c_id
        op['title']=window.prompt('Are you changing your title from '+c['title']+' ? ', c['title'])
        c['title']=op['title']
        op['Message']=window.prompt('Are you changing your message from '+c['message']+' ?',c['message'])
        c['message']=op['Message']
        op['S_date']=window.prompt('Are you changing '+op['title']+"'s Start date from "+c['s_date']+' ?',c['s_date'])
        c['s_date']=op['S_date']
        op['E_date']=window.prompt('Are you changing '+op['title']+"'s End date from "+c['e_date']+' ?',c['e_date'])
        c['e_date']=op['E_date']
        op['Budget']=Number(window.prompt('Are you changing '+op['title']+"'s Budget from ₹"+c['budget']+' ?',c['budget']))
        c['budget']=op['Budget']
        op['Niche']=window.prompt('Are you changing'+op['title']+"'s Niche from "+c['niche']+' ?',c['niche'])
        c['niche']=op['Niche']
        const put_req=await fetch(
            this.url+'/api/camps',
            {
                method:'PUT',
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": sessionStorage.getItem("token")
                  },
                  body: JSON.stringify(op)
            }
        )
    },
    async upad(ad){
        ad.Status='Pending'
        let ind=0
        for(var i=0;i<this.camps.length;i++){
           if (ad.C_id==this.camps[i].c_id){
            ind=i
           }
        }
        let prev=ad.Negotiated
        ad.Negotiated=window.prompt("Are you changing"+ ad.Title + "Negotiated price from ₹" + ad.Negotiated +' ? ',ad.Negotiated)
        if (ad.Negotiated > this.camps[ind].budget){
            window.alert("Your Price is higher than your campaign's budget. Change any of those")
            ad.Negotiated=prev
        }
        else{
        ad['bud']=this.camps[ind].budget
        const put_req=await fetch(this.url+'/api/ads',{method:'PUT',headers: {"Content-Type": "application/json","Authentication-Token": sessionStorage.getItem("token")},body: JSON.stringify(ad)})}
    },
    async acc(ad){
        ad.Salary=ad.Negotiated
        ad.Status='Paid'
        const put_req=await fetch(this.url+'/api/ads',{method:'PUT',headers: {"Content-Type": "application/json","Authentication-Token": sessionStorage.getItem("token")},body: JSON.stringify(ad)})
    },
    async exp(){
        const start_job=await fetch(this.url+'/csv')
        let tj=await start_job.json()
        let tid=tj.task_id
        window.open(this.url+'/fetc/'+tid)
    }
},
async mounted(){
    const url=window.location.origin
    const val=await fetch(url+'/api/spons',{
        headers: {
          "Authentication-Token": sessionStorage.getItem("token"),
        },
      })
    if (val.ok){
        let info=await val.json()
        info=info[0]
        this.name=info.name
        this.ind=info.ind
        this.email=info.email
        this.flag=info.flag
        this.approval=info.approval
        this.site=info.site
    }
    const val_camps=await fetch(url + '/api/camps',{
        headers: {
          "Authentication-Token": sessionStorage.getItem("token"),
        },
      })
   if (val_camps.ok){
    let cinfo=await val_camps.json()
    this.camps=cinfo
   }
   const val_ads = await fetch(url+'/api/ads',{
    headers: {
      "Authentication-Token": sessionStorage.getItem("token"),
    },
  } )
   if(val_ads.ok){
    let ainfo=await val_ads.json()
    this.ads=ainfo
   }
   
}
}
export default spons_profile