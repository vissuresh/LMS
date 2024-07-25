import { createRouter, createWebHistory } from 'vue-router'
import BooksView from '@/views/BooksView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import BookView from '@/views/BookView.vue'
import Navbar from '@/components/Navbar.vue'
import LibrarianNavbar from '@/components/LibrarianNavbar.vue'
import LibrarianDashboard from '@/views/librarian/LibrarianDashboard.vue'
import LibrarianBooksView from '@/views/librarian/book/LibrarianBooksView.vue'
import LibrarianBookAddView from '@/views/librarian/book/LibrarianBookAddView.vue'
import LibrarianBookEditView from '@/views/librarian/book/LibrarianBookEditView.vue'
import LibrarianSectionsView from '@/views/librarian/section/LibrarianSectionsView.vue'
import LibrarianSectionEditView from '@/views/librarian/section/LibrarianSectionEditView.vue'
import LibrarianSectionAddView from '@/views/librarian/section/LibrarianSectionAddView.vue'
import LibrarianBookRequestsView from '@/views/librarian/request/LibrarianBookRequestsView.vue'
import LibrarianBookIssuesView from '@/views/librarian/issue/LibrarianBookIssuesView.vue'
import SectionView from '@/views/SectionView.vue'
import store from '@/store'
import axios from 'axios'


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
      },
      {
        path:"books/:bookId",
        name: 'LibrarianBookEdit',
        components: {
          default: LibrarianBookEditView,
          navbar: LibrarianNavbar
        },
      },
      {
        path:"books/add",
        name: "LibrarianBookAdd",
        components: {
          default: LibrarianBookAddView,
          navbar: LibrarianNavbar
        },
      },
      {
        path: "sections",
        name: "LibrarianSections",
        components: {
          default: LibrarianSectionsView,
          navbar: LibrarianNavbar
        },
      },
      {
        path: "sections/:sectionId",
        name: "LibrarianSectionEdit",
        components: {
          default: LibrarianSectionEditView,
          navbar: LibrarianNavbar
        },
      },
      {
        path: "sections/add",
        name: "LibrarianSectionAdd",
        components: {
          default: LibrarianSectionAddView,
          navbar: LibrarianNavbar
        },
      },
      {
        path: "book-requests",
        name: "LibrarianBookRequests",
        components: {
          default: LibrarianBookRequestsView,
          navbar: LibrarianNavbar
        },
      },
      {
        path: "book-issues",
        name: "LibrarianBookIssues",
        components: {
          default: LibrarianBookIssuesView,
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
        name: 'RegisterView',
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



async function isLibrarian(userRole, to) {
  if(userRole === 'librarian' && to.path.includes('librarian')) {
    try {
      await axios.get('auth/isLibrarian');
      return true;
    } catch(error) {
      console.log(error);
      return false;
    }
  }
  return true;
}


router.beforeEach( async (to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated;
  const userRole = store.getters.isLibrarian ? 'librarian' : 'user';

  if(!isAuthenticated){
    if(to.name !== 'login' && to.name !== 'RegisterView'){
      next('/auth/login');
    }
    else{
      next();
    }
  }

  else if(to.name === 'login' || to.name === 'RegisterView'){
    next('/');
  }

  else if (to.meta.roles && !to.meta.roles.includes(userRole)) {
    next('/')
  }
  
  else {
    const canProceed = await isLibrarian(userRole, to);
    if(canProceed) {
      next();
    } else {
      next('/');
    }
  }
  
});

export default router