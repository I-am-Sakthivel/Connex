import router from "../utils/router.js";
const requests={
    template:`
    <div>
    <div class="card text-bg-info mb-3" style="max-width: 18rem;" v-for="ad in ads">
        <div class="card-header">
            {{ad.Title}}
        </div>
        <div class="card-body">
            <h5 class="card-title"> Negotiated: ₹{{ad.Negotiated}}</h5>
            <p class="card-text"> {{ad.Message}} </p>
            <div v-if="ad.Status!='Paid'">
                <div class="card-text" v-if="n"> 
                    <input type="number" v-model='ad.Negotiated' required>
                </div>
                <div v-if="ad.Status=='Pending'">
                    <button class="btn btn-success" @click="acc(ad)"> Accept </button>
                    <button class="btn btn-danger" @click="rej(ad)"> Reject </button>
                    <div>
                        <button class="btn btn-warning" @click="neg(ad)" v-if="(ad.Status!='Negotiated') & (n!=true) "> Negotiate </button>
                        <button class="btn btn-info" @click="conf(ad)" v-if="n"> confirm </button>
                    </div>
                </div>
            </div>
            <div v-if="ad.Status=='Paid'">
                <p>This is advertisment has been confirmed</p>
            </div>
            <div v-if="ad.Status=='Negotiated'">
                <p>Please wait till Sponsor's reply</p>
            </div>
        </div>
    </div>
</div>
    `,
    data()
    {
        return{
            ads:[],
            tem:{},
            n:false,
            temp:false
        }
    },
    methods:{
        async acc(ad){
            ad.Status='Paid'
            ad.Salary=ad.Negotiated
            const url=window.location.origin
            const fet_req= await fetch(url+'/api/ads',{method:'PUT',headers: {"Content-Type": "application/json","Authentication-Token": sessionStorage.getItem("token")},body: JSON.stringify(ad)})

        },
        async neg(ad){
            this.n=!this.n
        },
        async conf(ad){
            ad.Status="Negotiated"
            const url=window.location.origin
            const fet_req= await fetch(url+'/api/ads',{method:'PUT',headers: {"Content-Type": "application/json","Authentication-Token": sessionStorage.getItem("token")},body: JSON.stringify(ad)})
            this.n=!this.n
        },
        async rej(ad){
            const url=window.location.origin
            const fet_req= await fetch(url+'/api/ads',{method:'DELETE',headers: {"Content-Type": "application/json","Authentication-Token": sessionStorage.getItem("token")},body: JSON.stringify(ad)})
            const ind=this.ads.indexOf(ad)
            this.ads.splice(ind,1)
        }
    },
async mounted(){
    const url=window.location.origin
    const val=await fetch(url+'/api/ads',{headers:{"Authentication-Token": sessionStorage.getItem("token")},})
    if(val.ok){
        let ads=await val.json()
        this.ads=ads.ads
    }
    const seen=await fetch(url+'/turntoseen',{headers:{"Authentication-Token": sessionStorage.getItem("token")},})
}
}
export default requests;