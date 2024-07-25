import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
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
      store.dispatch('authenticated', true);


      // If user is librarian, set librarian to true
      if(response.data.is_librarian === true){
        store.dispatch('librarian', true);
      }

      // Retry the original request
      return axios(error.config);  
    }
    
    // If refresh token is invalid
    catch (e) {}

  }

  else if (error.response.status === 401) {
    router.push('/auth/login');
    
    store.dispatch('authenticated', false);
    store.dispatch('librarian', false);

  }


  else if(error.response.status === 403){
    store.dispatch('librarian', false);
    store.dispatch('authenticated', false);

    router.push('/');
  }
  
  return Promise.reject(error);

});
  

createApp(App).use(router).use(store).mount('#app')