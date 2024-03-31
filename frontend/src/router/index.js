import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterVue.vue'
import { useStore } from 'vuex'

const homeRoutes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    // beforeEnter: (to, from, next) => {
    //   const store = useStore();
    //   if (store.getters.isAuthenticated) {
    //     next();
    //   } else {
    //     next('/auth/login');
    //   }
    // },
  },
]

const authRoutes = [
  {
    path: '/auth',
    redirect: '/auth/login',
    children: [
      {
        path: 'login',
        name: 'login',
        component: LoginView,
        beforeEnter: (to, from, next) => {
          const store = useStore();
          if (store.getters.isAuthenticated) {
            next('/');
          } else {
            next();
          }
        },
      },
      {
        path: 'register',
        name: 'register',
        component: RegisterView,
        beforeEnter: (to, from, next) => {
          const store = useStore();
          if (store.getters.isAuthenticated) {
            next('/');
          } else {
            next();
          }
        },
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