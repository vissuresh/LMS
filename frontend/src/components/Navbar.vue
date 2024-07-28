<template>
  <nav class="navbar navbar-expand-lg bg-light mb-5">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">E-Library</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav navbar-right">
          <li class="nav-item" v-if="isAuthenticated">
            <router-link :to="{name: 'SectionsView'}">Sections</router-link>
          </li>
          <li class="nav-item" v-if="isAuthenticated">
            <router-link :to="{name: 'ProfileView'}">Profile</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <button class="btn btn-danger" v-if="isAuthenticated" @click="handleLogout">Logout</button>
            <router-link v-else to="/auth/login">Login</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import axios from 'axios';
import { createInfoModal } from '@/services/modal';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { computed } from 'vue';

const router = useRouter();
const store = useStore();

const isAuthenticated = computed(() => store.state.authenticated);

const handleLogout = async () => {
  let modal = null;

  try {
      const response = await axios.get('auth/logout');
      modal = createInfoModal('Logout', "Logout successful");
      
  } catch (error) {
      console.error('Error:', error);
      modal = createInfoModal('Logout', "Logout failed");
  }

  store.dispatch('authenticated', false);
  store.dispatch('librarian', false);

  modal.show();
  router.push('/auth/login');
};

</script>


<style scoped>
nav {
  padding: 12px;
  margin-bottom: 10px;
}

nav .navbar-brand {
  font-size: xx-large;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  font-size: larger;
}

nav a.router-link-exact-active {
  color: #42b983;
}

ul{
  list-style-type: none;
  margin: 0;
  padding: 0;
}

li {
  display: inline;
  padding: 8px;
}
</style>