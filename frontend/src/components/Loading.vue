<template>
    <div class="loader-overlay" v-if="isLoading">
      <div class="spinner-border text-secondary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    
</template>


<script setup>
import { defineProps } from 'vue';
const props = defineProps({
  isLoading: Boolean
});
</script>


<style scoped>
.loader-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1050;
}
</style>