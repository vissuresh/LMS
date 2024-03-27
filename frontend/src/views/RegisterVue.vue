<template>
  <div class="container ">
    <div class="row justify-content-center ">
      <div class="col-5 ">

        <div class="card">
          <div class="card-header"><h4>Register</h4></div>

          
          <form @submit.prevent="validate">
            <div class="card-body">

              <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input type="text" class="form-control" id="name" v-model="name" required>
              </div>

              <div class="mb-3">
                <label for="email" class="form-label">Email address</label>
                <input type="email" class="form-control" id="email" v-model="email" aria-describedby="emailHelp" required>
                <div id="emailHelp" class="form-text">We take privacy seriously.</div>
              </div>


            
            </div>

            <div class="card-body">
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" v-model="password" id="password" required>
              </div>

              <div class="mb-3">
                <label for="repassword" class="form-label">Re-enter Password</label>
                <input type="password" class="form-control" v-model="repassword" id="repassword" required>
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
const repassword = ref('');
const name = ref('');


const validate = () => {
  if(password.value != repassword.value){
    alert("Passwords do not match. Try again.");
    return;
  }
  register();
};


const register = async () => {
  try {
    const response = await axios.post('http://localhost:5000/auth/register', {
      email: email.value,
      password: password.value,
      name: name.value,
    });

    
    console.log('Response:', response);
    alert(response.data.message)
    router.push('/login');

  } catch (error) {
    console.error('Error:', error);
    alert(error.response.data.message);
  }
};
</script>
