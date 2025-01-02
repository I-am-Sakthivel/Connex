import router from "../utils/router.js"
const prof={
    template:`
    <div>
    This should not be visible
    </div>`,
    data(){
        return{
            logged:false,
            role:'',
        }
    },
    async mounted(){
        const url=window.location.origin
        const val=await fetch(url+'/profile')
        if (val.ok){
            let info=await val.json()
            this.logged=true
            this.role=info.role
            sessionStorage.setItem("token", info.token);
            switch(this.role){
                case 'Inf':{
            router.push('/inf/profile')
            break;
            }
            case 'Spons':{
                router.push('/spons/profile')
                break;
            }
            case 'Admin':{
                router.push('/admin/profile')
            }
        }
        }
    },
}
export default prof 