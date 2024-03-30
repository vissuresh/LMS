// src/services/logout.js
import axios from 'axios';

export async function logout(store, router) {
  if (store.getters.isAuthenticated) {
    try {
        const response = await axios.get('auth/logout');
        store.dispatch('updateAuthenticated', false);
    
        console.log('Response:', response);
        alert(response.data.message);
    
      } catch (error) {
        console.error('Error:', error);
        alert(error.response.message);
      }
  }
  router.push('/auth/login');
}