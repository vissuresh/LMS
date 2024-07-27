<template>
    <div class="card mb-3">
      <div class="card-body d-flex justify-content-between align-items-center">
        <div>
          <h5 class="card-title">{{ section.name }}</h5>
          <p class="card-text">{{ section.desc }}</p>
        </div>
        <router-link :to="{name: 'BooksView', query: {section_id: section.id}}"  class="btn btn-primary">View Books</router-link>
      </div>
    </div>
  </template>
  
  
<script setup>
import { defineProps } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

defineProps({
    section: {
        type: Object,
        required: true
    }
});

</script>

<style scoped>
.card {
    margin-bottom: 1rem;
}
</style>