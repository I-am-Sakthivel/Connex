const ser={
    template:
    `<div style="position: absolute; top: 150px; right: 750px;">
    <span>
    <input type="text" v-model="se"/>
    <button class='btn btn-danger' @click='show()'>Search</button>
    <div v-if="role=='Inf'">
    <div class="card text-primary mb-3" style="max-width: 18rem;" v-for="val in camps_show">
    <div class="card-header">
        Title: {{val.title}}
    </div>
    <div class="card-body">
    <div class="card-header">Sponsor: {{val.name}}</div>
       <p class="card-text"> Message:{{val.message}}</p>
       <p class="card-text"> <span>Starts on <p style="color:green">{{val.s_date}}</p> </span> </p> <p class="card-text"> <span>Ends on <p style="color:red">{{val.e_date}}</p> </span> </p>  </p>
       <p class="card-text" v-if="val.part=='true'" style="color:red"> You have already took part in this campaign </p>
       <p class="card-text" v-if="val.part=='false'" style="color:green"> You have not took part in this campaign </p>
       <span>
       <p class="card-text" style="color:gold">{{val.niche}}</p>
       <p class="card-text"> Budget: ₹{{val.budget}}</p>
       </span>
       <button class='btn btn-warning' @click='req(val)'>Request </button>
    </div>
</div>  
    </div>
    <div v-if="role=='Spons'">
    <div class="card text-bg-primary mb-3" style="max-width: 18rem;" v-for="val in inf_show">
    <div class="card-header">
        Name: {{val.name}}
    </div>
    <div>
       <p class="card-text" style="color:red">Niche:{{val.niche}} </p>
       <p class="card-text" style="color:green"> Reach:{{val.reach}}</p>
       <span>
       <p class="card-text" style="color:gold">{{val.category}}</p>
       <a class="card-text" :href="val.site"> visit site </a>
       </span>
       <button class='btn btn-warning' @click='req_inf(val)'>Request </button>
    </div>
</div>
    </div>
    </span>
    </div>`,
data(){
    return{
        se:"",
        camps:[],
        role:"",
        infs:[],
        camps_show:[],
        inf_show:[],
        email:"",
        cs:[]
    }
},
methods:{
    show(){
        this.camps_show=[]
        this.camps.forEach(camp => {
            if(camp.title==this.se){
                this.camps_show.push(camp)  
            }
        });
        this.inf_show=[]
        this.infs.forEach(inf => {
            if(inf.name==this.se){
                this.inf_show.push(inf)  
            }
        });
    },
    async req(c){
        let ad={}
            ad.title=window.prompt('What is the title you are proposing ? ')
            ad.Message=window.prompt('What message would you like to post to the Sponsor ?')
            ad.Negotiated=window.prompt("What is your negotiated pay? note: The campaign's total budget is ₹"+c.budget)
            if (ad.title==null){
                ad.title=c.title
            }
            if(ad.Message==null){
                ad.Message=c.message
            }
            if(ad.Negotiated==null| ad.Negotiated>=c.budget){
                ad.Negotiated=0
            }
            ad.C_id=c.c_id
            ad.I_email=this.email
            ad.salary=0
            ad.Status='Negotiated'
            const url=window.location.origin
            const val= await fetch(
                url+'/api/ads',
                {
                    method:'POST',
                    headers: {
                        "Content-Type": "application/json",
                        "Authentication-Token": sessionStorage.getItem("token"),
                      },
                      body: JSON.stringify(ad)
                })
    },
    async req_inf(inf){
        let ad={}
        ad.C_id=window.prompt("enter your campaign id ")
        ad.title=window.prompt('What is the title you are proposing ? ')
        ad.Message=window.prompt('What message would you like to post to the Influencer ?')
        ad.Negotiated=window.prompt("What is your negotiated pay? keep the campaign's budget in mind")
        ad.I_email=inf.email
        ad.salary=0
        ad.Status='Pending'
        const url=window.location.origin
            const val= await fetch(
                url+'/api/ads',
                {
                    method:'POST',
                    headers: {
                        "Content-Type": "application/json",
                        "Authentication-Token": sessionStorage.getItem("token"),

                      },
                      body: JSON.stringify(ad)
                })

    }
},
async mounted(){
    const url=window.location.origin
    const data=await fetch(url+'/search',{
        headers: {
          "Authentication-Token": sessionStorage.getItem("token"),
        },
      }
    )
    if (data.ok){
        let info=await data.json()
        this.role=info.role
        this.email=info.email
        if (this.role=='Inf'){
            this.camps=info.res
        }
        else{
            this.infs=info.res
        }
    }
}
}
export default ser