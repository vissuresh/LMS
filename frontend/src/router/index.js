import { createRouter, createWebHistory } from 'vue-router'
import BooksView from '@/views/BooksView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterVue.vue'
import BookView from '@/views/BookView.vue'
import Navbar from '@/components/Navbar.vue'
import LibrarianNavbar from '@/components/LibrarianNavbar.vue'
import LibrarianBooksView from '@/views/librarian/LibrarianBooksView.vue'
import LibrarianDashboard from '@/views/librarian/LibrarianDashboard.vue'
import SectionView from '@/views/SectionView.vue'
import store from '@/store'


const defaultRoute ={
  path: '/',
  redirect: () => {
    const userRole = store.getters.isLibrarian ? 'librarian' : 'user';
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
    meta: { roles: ['user', 'librarian']},
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
        path: '',
        name: 'LibrarianDashboard',
        components: {
          default: LibrarianDashboard,
          navbar: LibrarianNavbar
        },
      },
      {
        path: 'books',
        name: 'LibrarianBooks',
        components: {
          default: LibrarianBooksView,
          navbar: LibrarianNavbar
        },
      }
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
  defaultRoute, ...authRoutes, ...bookRoutes, ...librarianRoutes, ...sectionRoutes
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated;
  const userRole = store.getters.isLibrarian ? 'librarian' : 'user';

  if(!isAuthenticated){
    if(to.name !== 'login' && to.name !== 'register'){
      next('/auth/login');
    }
    else{
      next();
    }
  }

  else if(to.name === 'login' || to.name === 'register'){
    next('/');
  }

  else if (to.meta.roles && !to.meta.roles.includes(userRole)) {
    next('/')
  }
  
  else {
    next();
  }
  
});

export default router