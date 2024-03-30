import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterVue.vue'

const homeRoutes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  }, 
]

const authRoutes = [
  {
    path: '/auth',
    component: { render: h => h('router-view') },
    redirect: '/auth/login',
    children: [
      {
        path: 'login',
        name: 'login',
        component: LoginView,
      },
      {
        path: 'register',
        name: 'register',
        component: RegisterView,
      },
    ]
  }
]


const routes = [
  ...authRoutes, ...homeRoutes
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router