import { createApp } from 'vue'
import './style.css'
import router from './router'
import App from './App.vue'
import LoginCallback from './components/LoginCallback.vue'
import Login from './components/Login.vue'

const app = createApp(App)
app.component('LoginCallback', LoginCallback)
app.component('Login', Login)
app.use(router)
app.mount('#app')
