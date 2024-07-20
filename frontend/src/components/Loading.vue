<template>
    <div class="loader-overlay" v-if="isLoading">
        <div class="loader"></div>
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

.loader {
    border: 7px solid #f3f3f3;
    border-top: 7px solid #0bd998;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 2s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>