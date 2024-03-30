<template>
  <nav class="navbar navbar-expand-lg bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">E-Library</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav navbar-right">
          <li class="nav-item">
            <router-link to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/auth/logout" @click="logout">Logout</router-link>
            <router-link to="/auth/login">Login</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { logout } from '@/services/logout';
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