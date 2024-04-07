<template>
  <router-view name="navbar"/>
  <router-view />
  <InfoModal />
</template>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>


<script>
import Navbar from './components/Navbar.vue'
import InfoModal from './components/InfoModal.vue'

export default {
  name: 'App',
  components: {
    Navbar, InfoModal
  }
}
</script>