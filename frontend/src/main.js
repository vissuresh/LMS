import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import createInfoModal from './services/modal.js'
import store from './store'

import 'bootstrap/dist/css/bootstrap.css'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.js'


axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000/';

axios.interceptors.response.use(undefined, async function (error) {

  if (error.response.status === 401 && error.config && !error.config.url.endsWith('auth/refresh'))
  {

    try {
      const response = await axios.get('auth/refresh');
      localStorage.setItem('authenticated', true);

      if(response.data.is_librarian === true){
        localStorage.setItem('librarian', true);
      }

      return axios(error.config);  
    } 
    catch (e) {
      router.push('/auth/login');
    }

  }
  return Promise.reject(error);

});
  

createApp(App).use(store).use(router).mount('#app')