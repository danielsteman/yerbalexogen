import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import LoginCallback from '../components/LoginCallback.vue'
const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/login/callback',
    component: LoginCallback
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router