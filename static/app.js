import router from './utils/router.js';
import Navbar from './components/Navbar.js';
import requests from './pages/requests.js';
new Vue({
    el:'#app',
    template:`
    <div>
    <Navbar/>
    <router-view/>
    </div>`,
    router,
    components:{
        Navbar,
        requests
    }
})
