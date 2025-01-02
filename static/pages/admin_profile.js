import router from "../utils/router.js"
const admin_profile={
template:`
<div>
        <h1>Welcome {{name}}</h1>
        <table class='table-warning table-bordered'>
        <caption>Sponsors</caption>
         <tr>
        <th scope="col">Name</th>
        <th scope="col">email_id</th>
        <th scope="col">Industry</th>
        <th scope="col">Flag</th>
        <th scope="col">Approval</th>
        <th scope="col">site</th>
        </tr>
            <tr v-for="s in sp_info"> 
               <th>{{s.name}}</th>
               <td>{{s.email}}</td>
               <td>{{s.ind}}</td>
               <td>
             <button :class="[s.flag=='True'? 'btn-danger' :'btn-success']" @click="flag(s)"> <p v-if="s.flag=='True'">Flag</p> <p v-else> Unflag</p>    </button>
               </td>
               <td>
               <div v-if="s.Approval=='False'">
               <div class='table-success'> <button @click="app(s)" class='btn-success'> Approve </button> </div>
               </div>
               <div v-else>
               <div class='table-success'>Approved </div>
               </div>
               </td>
               <td><button @click="visit(s.site)" class='btn-success'>Visit site </button></td>        
            </tr>
        </table>
      <table class='table-primary table-bordered'>
    <caption class="caption">Influencers</caption>
    <tr>
        <th scope="col">Name</th>
        <th scope="col">email</th>
        <th scope="col">Category</th>
        <th scope="col">Niche</th>
        <th scope="col">Reach</th>
        <th scope="col">Balance</th>
        <th scope="col">Flag</th>
        <th scope="col">Site</th>
        </tr>
        <tr v-for="i in inf_info"> 
            <td scope="row">{{i.name}}</td>
            <td >{{i.email}}</td>
            <td >{{i.category}}</td>
            <td >{{i.niche}}</td>
            <td>{{i.reach}}</td>
            <td>     {{i.balance}}</td>
            <div v-if="i.flag=='False'">
            <div class='table-danger'> <button @click="flag_inf(i)" class='btn-success'> Unflag </button> </div>
               </div>
            <div v-else>
            <div class='table-danger'> <button @click="flag_inf(i)" class='btn-danger'> Flag </button> </div>
            </div>
            <td ><button @click="visit(i.site)" class='btn-success'>Visit site </button></td>
        </tr>
</table>
<table class='table-primary table-bordered'>
    <caption class="caption">Campaingn</caption>
    <tr>
        <th scope="col">C_id</th>
        <th scope="col">Sponsor</th>
        <th scope="col">title</th>
        <th scope="col">Message</th>
        <th scope="col">S_date</th>
        <th scope="col">E_date</th>
        <th scope="col">Budget</th>
        <th scope="col">Niche</th>
        <th scope="col">Flag</th>
        </tr>
        <tr v-for="c in camp_info"> 
            <td scope="row">{{c.c_id}}</td>
            <td >{{c.name}}</td>
            <td >{{c.title}}</td>
            <td>{{c.message}}</td>
            <td >{{c.s_date}}</td>
            <td >{{c.e_date}}</td>
            <td>{{c.budget}}</td>
            <td>{{c.niche}}</td>
            <div v-if="c.flag=='False'">
            <div class='table-danger'> <button @click="flag_camp(c)" class='btn-success'> Unflag </button> </div>
               </div>
            <div v-else>
            <div class='table-danger'> <button @click="flag_camp(c)" class='btn-danger'> Flag </button> </div>
            </div>
        </tr>
</table>
    </div>
`,
data (){
    return {
        ads:[],
        camps:[],
        name:'',
        spons:[],
        text:'',
        inf:[],
        sp_info:[],
        inf_info:[],
        camp_info:[],
        text_f:'Unflag',
        text_t:'flag'
    }},
    methods:
    {
        async flag(fl){
            //this is to update the details for sposnsors.
            if (fl.flag=='True'){
                fl.flag='False'
             }
             else{
                fl.flag='True'
             }
            const url=window.location.origin
            const req= await fetch(url+'/api/spons',{
                method:"PUT",headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": sessionStorage.getItem("token")
                  },body:JSON.stringify({"Flag":fl.flag,"email":fl.email})})
                
        },
        visit(l){
            window.open(l)
        },
        async flag_inf(fl){
            if (fl.flag=='True'){
                fl.flag='False'
             }
             else{
                fl.flag='True'
             }
            const url=window.location.origin
            const req= await fetch(url+'/api/inf',{
                method:"PUT",headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": sessionStorage.getItem("token")
                  },body:JSON.stringify({"Flag":fl.flag,"email":fl.email})})
        },
        async app(bl){
            const url=window.location.origin
            const req= await fetch(url+'/api/spons',{
                method:"PUT",headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": sessionStorage.getItem("token")
                  },body:JSON.stringify({"Approval":'True',"email":bl.email})})
        },
        async flag_camp(fl){
            if (fl.flag=='True'){
                fl.flag='False'
             }
             else{
                fl.flag='True'
             }
            const url=window.location.origin
            const req= await fetch(url+'/api/camps',{
                method:"PUT",headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": sessionStorage.getItem("token")
                  },body:JSON.stringify({"Flag":fl.flag,"C_id":fl.c_id})})
        }
    },
 async mounted(){
    const url=window.location.origin
    const val_spons=await fetch(url+'/api/spons',{
        headers: {
          "Authentication-Token": sessionStorage.getItem("token"),
        },
      })
    const val_admin=await fetch(url+'/profile',{
        headers: {
          "Authentication-Token": sessionStorage.getItem("token"),
        },
      })
    const val_inf=await fetch(url + '/api/inf',{
        headers: {
          "Authentication-Token": sessionStorage.getItem("token"),
        },
      })
    const val_camps=await fetch(url+'/api/camps',{
        headers: {
          "Authentication-Token": sessionStorage.getItem("token"),
        },
      })
    if (val_spons.ok){
       const sinfo=await val_spons.json()
        this.sp_info=sinfo
    }
    if (val_admin.ok){
        const ainfo=await val_admin.json()
        this.name=ainfo.name
    }
    if (val_inf.ok){
        const iinfo=await val_inf.json()
        this.inf_info=iinfo
    }
    if (val_camps.ok){
        const cinfo=await val_camps.json()
        this.camp_info=cinfo
    }
 }
}
export default  admin_profile