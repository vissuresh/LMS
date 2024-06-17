import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

import 'bootstrap/dist/css/bootstrap.css'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.js'


axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000/';

axios.interceptors.response.use(undefined, async function (error) {

  if (error.response.status === 401 && error.config && !error.config.url.endsWith('auth/refresh'))
  {

    // Try to get new access token
    try {
      const response = await axios.get('auth/refresh');
      localStorage.setItem('authenticated', true);


      // If user is librarian, set librarian to true
      if(response.data.is_librarian === true){
        localStorage.setItem('librarian', true);
      }

      // Retry the original request
      return axios(error.config);  
    }
    
    // If refresh token is invalid, redirect to login
    catch (e) {
      router.push('/auth/login');
    }

  }

  // if not 401 or no error config or is a refresh request
  return Promise.reject(error);

});
  

createApp(App).use(router).mount('#app')