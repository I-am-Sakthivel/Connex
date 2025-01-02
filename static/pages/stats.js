const stat={
template:`<div>



<div v-if="role=='Inf'">
<h1> A few important Statistics </h1>
<div style="position: absolute; top: 250px; right: 800px;">
<h3> Descriptive Statistics of your data </h3>
<p> (Don't worry if your salaries seem low, this analysis is prepared only with confirmed adverts) </p> 
<h5> On average you earn about <p style="color:maroon"> ₹{{Inf_stat.mean}} </p> </h5>
<h5> Your Median salary is <p style="color:green"> ₹{{Inf_stat.median}} </p> </h5>
<h5> Your Maximum Salary<p style="color:blue"> ₹{{Inf_stat.max_sal}} </p> </h5>
<h5> You frequently Collaborate with <p style="color:red"> {{Inf_stat.spons_name[0]}} </p> </h5>
</div>
</div>

<div v-if="role=='Spons'">
<h1> A few important Statistics </h1>
<div style="position: absolute; top: 250px; right: 800px;">
<h3> Descriptive Statistics of your data </h3>
<h5> Your most participated Campaign is <p style="color:green"> {{spons_stat.camp[0]}} </p> </h5>
<h5> You have spent most of your money in <p style="color:red"> {{spons_stat.msp[0]}} </p> </h5>
<h5> Your have worked mostly with <p style="color:maroon"> {{spons_stat.names[0]}} </p> </h5>
</div>
</div>



<div v-if="role=='Admin'">
<h1> A few important Statistics </h1>
<div style="position: absolute; top: 250px; right: 800px;">
  <h5> Influencer with most adverts : <h5 style="color:maroon">{{admin_stat.inf_n[0]}} </h5> </h5>
  <h5> Influencer with the highest balance: <h5 style="color:blue">{{admin_stat.inf_s[0]}} </h5> </h5>
  <h5> Campaign with the highest number of Adverts: <h5 style="color:red">{{admin_stat.cp_n[0]}} </h5> </h5>
  <h5> Campaign with most money spent : <h5 style="color:green">{{admin_stat.cp_s[0]}} </h5> </h5>
  <h5> Sponsor of the most expensive Campaign : <h5 style="color:purple">{{admin_stat.sp_max_budget[0]}} </h5> </h5>
</div>
</div>



</div>
`,
data(){
    return{
        role:"",
        Inf_stat:{},
        spons_stat:{},
        admin_stat:{}
    }
},
async mounted(){
    const url=window.location.origin
    const d=await fetch(url+'/stats',{headers:{"Authentication-Token": sessionStorage.getItem("token")}})
    if(d.ok){
        let da=await d.json()
        this.role=da.role
        if (this.role=='Inf'){
            this.Inf_stat=da
        }
        else if (this.role=='Spons'){
            this.spons_stat=da
        }
        else{
            this.admin_stat=da
        }
    }
}
}
export default stat;