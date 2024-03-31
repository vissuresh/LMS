import { createApp, registerRuntimeCompiler } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

import 'bootstrap/dist/css/bootstrap.css'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.js'
import store from './store'

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000/';

axios.interceptors.response.use(undefined, async function (error) {
  if (error.response.status === 401 && error.config && !error.config.__isRetryRequest)
  {
    if (document.cookie.split(';').some((item) => item.trim().startsWith('refresh_token_cookie=')))
    {
      try {
        await axios.get('auth/refresh');
        error.config.__isRetryRequest = true;
        return axios(error.config);
      } 
      catch (e) {
        
        if (e.response && e.response.status === 401) 
        {
          alert('Your session has expired. Please log in again.');
          router.push('/auth/login');
        }
        else {
          console.error(e);
          alert('An error occurred. Please try again later.');
        }

        return Promise.reject(error);
      }
    } 
    else if (error.response.status === 401)
    {
      console.log('AXIOS INTERCEPTOR for 401 error')
      store.dispatch('updateAuthenticated', false);
      router.push('/auth/login');
    }
    else if (error.response.status === 403)
    {
      console.log('INSIDE AXIOS INTERCEPTOR for 403 error')
      store.dispatch('updateAuthenticated', false);
      router.push('/auth/login');
    }
  }
  return Promise.reject(error);
});

createApp(App).use(store).use(router).mount('#app')
