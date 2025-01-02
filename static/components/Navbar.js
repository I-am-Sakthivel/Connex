const Navbar={
    template:`
    <nav>
    <router-link to='/' style="text-decoration:none"><h1 style="color:lilac" > Connex </h1></router-link>
    <div v-if="msg=='yes'">
    <a  href="/logout" style="position: absolute; top: 50px; right: 125px;">Logout</a>
    <router-link to='/stats' style="position: absolute; top: 20px; right: 1200px;"><button class="btn btn-warning">Stats</button></router-link>
    </div>
    </nav>`,
    data(){
        return {
            url:window.location.origin + '/logout',
            msg:""
        }
    },
    async mounted(){
        const url=window.location.origin
        const val=await fetch(url+'/aretheyloggedin')
        if(val.ok){
            this.msg=await val.json()
            this.msg=this.msg.message
        }
    }
}
export default Navbar;