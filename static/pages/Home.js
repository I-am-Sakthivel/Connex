import router from '../utils/router.js';
const Home={
    template:`
    <div>
    <h1> Welcome to home!! </h1>
    <p> Here we will show top performers and their testimonials</p>
    <div v-if="msg=='no'">
    <router-link to='/login' style="position: absolute; top: 250px; right: 800px;">Login</router-link>
    <router-link to='/signup' style="position: absolute; top: 300px; right: 790px;">Signup</router-link>
    </div>
    </div>
    `,
    data()
    {
        return{
            msg:""
        }
    },
async mounted(){
    const url=window.location.origin
    const val=await fetch(url+'/aretheyloggedin')
    if(val.ok){
        this.msg=await val.json()
        this.msg=this.msg.message
        if (this.msg=='yes'){
            router.push('/profile')
        } 
    }
}
}
export default Home;