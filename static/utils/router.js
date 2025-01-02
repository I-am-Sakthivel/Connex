import Home from '../pages/Home.js';
import login from '../pages/login_signup_logout.js'
import {signup,logout} from '../pages/login_signup_logout.js'
import influ_profile from '../pages/influ_profile.js';
import prof from '../pages/profile.js';
import admin_profile from '../pages/admin_profile.js';
import spons_profile from '../pages/spons_profile.js';
import crecam from '../components/cre_cam.js';
import requests from "../pages/requests.js";
import ser from '../pages/search.js';
import stat from '../pages/stats.js';
const routes=[
    {path:'/',component:Home},
    {path:'/login',component:login},
    {path:'/signup',component:signup},
    {path:'/logout',component:logout},
    {path:'/profile',component:prof},
    {path:'/inf/profile',component:influ_profile},
    {path:'/admin/profile',component:admin_profile},
    {path:'/spons/profile',component:spons_profile},
    {path:'/reqs',component:requests},
    {path:'/search',component:ser},
    {path:'/stats',component:stat}
]
const router=new VueRouter({routes,})
export default router