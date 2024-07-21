<template>
  <div class="container ">
    <div class="row justify-content-center">
      <div class="col-5 ">

        <div class="card">
          <div class="card-header text-center"><h4>Login</h4></div>

            <div class="card-body">  
              <div class="mb-3">
                <label for="email" class="form-label">Email address</label>
                <input type="email" class="form-control" id="email" v-model="email" required>
              </div>

              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" v-model="password" id="password" required>
              </div>
            </div>

            <div class="card-footer">
              <div class="row">
                
                <div class="col">
                  <button type="submit" class="btn btn-primary" @click="login">Submit</button>
                </div>

                <div class="col text-end">
                  <span>New user?<router-link :to="{name:'RegisterView'}" class="btn btn-link">Register here!</router-link> </span>
                </div>

              </div>
            </div>

        </div>

      </div>

    </div>
  </div>
</template>




<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { createInfoModal } from '@/services/modal.js';

const router = useRouter();
const store = useStore();

const email = ref('');
const password = ref('');


const login = async () => {
  try {
    const response = await axios.post('auth/login', {
      email: email.value,
      password: password.value
    });

    store.dispatch('authenticated', true);

    if(response.data.is_librarian === true)
    {
      store.dispatch('librarian', true);
      router.push('/librarian');
    } else 
    {  
      router.push('/books');  
    }

  } catch (error) {
    const modal = createInfoModal("Login", error.response.data.message);
    modal.show();
  }
};
</script>