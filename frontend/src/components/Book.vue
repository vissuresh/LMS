<template>
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{{ book.name }}</h5>
        <h6 class="card-subtitle mb-2 text-muted">{{ book.author }}</h6>
        <p class="card-text">{{ book.section.name }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, toRefs } from 'vue';
  
  const props = defineProps({
    book: {
      type: Object,
      default: () => ({})
    }
  });
  
  const { book } = toRefs(props);
  </script>
  
  <style scoped>
  .card {
    margin-bottom: 1em;
  }
  </style>