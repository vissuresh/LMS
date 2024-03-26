<template>
  <div class="container ">
    <div class="row justify-content-center ">
      <div class="col-5 ">

        <div class="card">
          <div class="card-header"><h4>Login</h4></div>

          <div class="card-body">
            <form @submit.prevent="login">

              <div class="mb-3">
                <label for="email" class="form-label">Email address</label>
                <input type="email" class="form-control" id="email" v-model="email" aria-describedby="emailHelp">
                <div id="emailHelp" class="form-text">We take privacy seriously.</div>
              </div>

              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" v-model="password" id="password">
              </div>

              <button type="submit" class="btn btn-primary">Submit</button>
            </form>

          </div>

        </div>

      </div>

    </div>
  </div>
</template>




<script setup>
import { ref } from 'vue';
import axios from 'axios';

const email = ref('');
const password = ref('');



const login = async () => {
  try {
    const response = await axios.post('http://localhost:5000/auth/login', {
      email: email.value,
      password: password.value
    });

    // Handle response data
    console.log('Response:', response.data);
  } catch (error) {
    console.error('Error:', error);
  }
};
</script>
