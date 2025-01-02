import router from "../utils/router.js"
const login={
    template:
    `<div v-if="appr" class="d-flex justify-content-center align-items-center vh-90">
      <div class="card shadow p-4 border rounded-3 ">
        <h3 class="card-title text-center mb-4">Login</h3>
        <div class="form-group mb-3">
          <input v-model="email" type="email" class="form-control" placeholder="Email" required/>
        </div>
        <div class="form-group mb-4">
          <input v-model="password" type="password" class="form-control" placeholder="Password" required/>
        </div>
        <button class="btn btn-primary w-100" @click="submitInfo">Submit</button>
      </div>
    </div>
    <div v-else>
    <h1>Uh oh! You are not approved yet</h1>
    </div>
    `,
    data(){
      return{
        email:"",
        password:"",
        appr:true
      }},
      methods:{
        async submitInfo(){
         const url=window.location.origin
          const req=await fetch(url+'/login',{
            method:'POST', 
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({email:this.email,password:this.password})
          })
          if (req.ok){
            router.push('/profile')
          }
          else{
            this.appr=false
            console.error("Login failed")
          }
        },
      },
}
const signup={
    template:
    `<div class="d-flex justify-content-center align-items-center vh-100">
    <div v-if="user">User exists</div>
      <div class="card shadow p-4 border rounded-3 ">
        <h3 class="card-title text-center mb-4">Signup</h3>
        <div class="form-group mb-3">
          <input v-model="name" type="text" class="form-control" placeholder="Name" required/>
        </div>
        <div class="form-group mb-3">
          <input v-model="email" type="email" class="form-control" placeholder="Email" required/>
        </div>
        <div class="form-group mb-4">
          <input v-model="password" type="password" class="form-control" placeholder="Password" required/>
        </div>
        <div class="form-group mb-4">
        <select v-model="role" class="form-control" text="Role"  >
            <option value="Inf">Influencer</option>
            <option value="Spons">Sponsor</option>
          </select>
          </div>
          <div v-if=" role=='Inf' ">
          <div class="form-group mb-4">
          <input v-model="Cat" type="text" class="form-control" placeholder="Category" required/>
          </div>
          <div class="form-group mb-4">
          <input v-model="Nic" type="text" class="form-control" placeholder="Niche" required/>
          </div>
          <div class="form-group mb-4">
          <input v-model="reach" type="text" class="form-control" placeholder="Reach" required/>
          </div>
          <div class="form-group mb-4">
          <input v-model="site" type="text" class="form-control" placeholder="site" required/>
          </div>
          </div>
          <div v-if="role=='Spons'" class="form-group mb-4">
          <div class="form-group mb-4">
          <input v-model="Ind" type="text" class="form-control" placeholder="Industry" required/>
          </div>
          <div class="form-group mb-4">
          <input v-model="site" type="text" class="form-control" placeholder="site" required/>
          </div>
          </div>
        <button class="btn btn-primary w-100" @click="register">Submit</button>
    </div>
    </div>
    `,
    data(){
      return{
        name:'',
        email:'',
        password:'',
        role:'',
        Cat:'',
        Nic:'',
        reach:'',
        Ind:'',
        site:''
      }
    },
    methods:
    {
      async register(){
      const url=window.location.origin
      let value={name:this.name,
        email:this.email,
        password:this.password,
        role:this.role,
        Cat:this.Cat,
        Nic:this.Nic,
        reach:this.reach,
        Ind:this.Ind,
      site:this.site}
      const req=await fetch(url+'/register',{
        method:'POST', 
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(value)
      })
      if (req.ok){
        router.push('/profile')
      }
      else{
        console.error('Signup Failed')
      }
    }
}}
const logout={
    template:
    ``
}
export default login;
export  {signup,logout};