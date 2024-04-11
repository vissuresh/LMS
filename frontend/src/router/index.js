import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterVue.vue'
import BookView from '../views/BookView.vue'
import Navbar from '@/components/Navbar.vue'
import LibrarianNavbar from '@/components/LibrarianNavbar.vue'
import Dashboard from '@/views/librarian/Dashboard.vue'
import SectionView from '@/views/SectionView.vue'

console.log(Navbar);


const bookRoutes = [
  {
    path: '/books',
    name: 'books',
    components: {
      default: HomeView,
      navbar: Navbar
    },
  },

  {
    path: '/books/:id',
    name: 'book',
    components: {
      default: BookView,
      navbar: Navbar
    },
    props: true,
  },
]


const sectionRoutes = [

  {
    path: '/sections/:id',
    name: 'sections',
    components: {
      default: SectionView,
      navbar: Navbar
    },
    props: true,
  },
]


const librarianRoutes = [
  {
    path: '/librarian',
    redirect: '/librarian',
    meta: { roles: ['librarian']},  

    children: [
      {
        path: '/',
        name: 'dashboard',
        components: {
          default: Dashboard,
          navbar: LibrarianNavbar
        },
      },
    ],
  }
]

const authRoutes = [
  {
    path: '/auth',
    redirect: '/auth/login',
    children: [
      {
        path: 'login',
        name: 'login',
        components: {
          default: LoginView,
          navbar: Navbar
        },
      },
      {
        path: 'register',
        name: 'register',
        components: {
          default: RegisterView,
          navbar: Navbar
        },
      },
    ]
  }
]




const routes = [
  ...authRoutes, ...bookRoutes, ...librarianRoutes, ...sectionRoutes
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


router.beforeEach((to, from, next) => {
  const userRole = localStorage.getItem('librarian') ? 'librarian' : 'user';
  if (to.meta.roles && !to.meta.roles.includes(userRole)) {
    next('/books');
  } else {
    next();
  }
});

export default router