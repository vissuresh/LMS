// src/services/logout.js
import axios from 'axios';
import { useRouter } from 'vue-router';

export async function logout() {
  const router = useRouter();

  if (localStorage.getItem('isAuthenticated')) {
    try {
        const response = await axios.delete('auth/logout');
        localStorage.removeItem('isAuthenticated');
    
        console.log('Response:', response);
        alert(response.data.message);
    
      } catch (error) {
        console.error('Error:', error);
        alert(error.response.data.message);
      }
  }
  router.push('/login');
}