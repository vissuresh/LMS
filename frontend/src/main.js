import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

import 'bootstrap/dist/css/bootstrap.css'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.js'
import store from './store'


axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000/';

axios.interceptors.response.use(undefined, async function (error) {
    if (error.response.status === 401 && error.config && !error.config.url.endsWith('/auth/refresh')) {
  
      if (document.cookie.split(';').some((item) => item.trim().startsWith('refresh_token_cookie='))) {
        // Checking if refresh token cookie is available
  
        try {
          await axios.get('auth/refresh');
          return axios.request(error.config);
          //  Retry the original request
  
        } catch (e) {}
      }
    }

    if (error.response.status === 401) {
        router.push('/auth/login');
    }

    return Promise.reject(error);
});

createApp(App).use(store).use(router).mount('#app')
