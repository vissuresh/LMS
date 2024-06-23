import { createRouter, createWebHistory } from 'vue-router'
import BooksView from '@/views/BooksView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterVue.vue'
import BookView from '@/views/BookView.vue'
import Navbar from '@/components/Navbar.vue'
import LibrarianNavbar from '@/components/LibrarianNavbar.vue'
import Dashboard from '@/views/librarian/Dashboard.vue'
import SectionView from '@/views/SectionView.vue'


const defaultRoute ={
  path: '/',
  redirect: () => {
    const userRole = localStorage.getItem('librarian') ? 'librarian' : 'user';
    if (userRole === 'user') {
      return '/books';

    } else if (userRole === 'librarian') {
      return '/librarian';
    }
  }
};


const bookRoutes = [
  {
    path: '/books',
    name: 'books',
    meta: { roles: ['user']},  

    components: {
      default: BooksView,
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
  defaultRoute, ...authRoutes, ...bookRoutes, ...librarianRoutes
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


router.beforeEach((to, from, next) => {
  const userRole = localStorage.getItem('librarian') ? 'librarian' : 'user';

  if (to.meta.roles && !to.meta.roles.includes(userRole)) {
    next('/')
  } else {
    next();
  }
  
});

export default router