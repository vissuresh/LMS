<template>
  <div class="container ">
    <div class="row justify-content-center ">
      <div class="col-5 ">

        <div class="card">
          <div class="card-header"><h4>Login</h4></div>

          
          <form @submit.prevent="login">
            <div class="card-body">  
              <div class="mb-3">
                <label for="email" class="form-label">Email address</label>
                <input type="email" class="form-control" id="email" v-model="email" required>
              </div>

              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" v-model="password" id="password" required>
              </div>

              <button type="submit" class="btn btn-primary">Submit</button>
            </div>

          </form>

        </div>

      </div>

    </div>
  </div>
</template>




<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

const email = ref('');
const password = ref('');




const login = async () => {
  try {
    const response = await axios.post('auth/login', {
      email: email.value,
      password: password.value
    });

    localStorage.setItem('isAuthenticated', true);
    console.log('Response:', response);
    alert(response.data.message);
    router.push('/');

  } catch (error) {
    console.error('Error:', error);
    alert(error.response.data.message);
  }
};
</script>