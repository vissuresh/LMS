<template>

    <div class="card text-center">
      <div class="card-header">
        Apply Filters
      </div>
      <div class="card-body">
        <ul class="list-group list-group-flush">
          <li class="list-group-item mb-5">
            <h5 class="card-title">Sections</h5>
            <Dropdown :options="sections" :title="'Sections'" />
          </li>
          <li class="list-group-item mb-5">
            <h5 class="card-title">Authors</h5>
            <Dropdown :options="authors" :title="'Authors'" />
          </li>

          <li class="list-group-item ">
            <h5 class="card-title">Rating</h5>
            <div class="btn-group btn-warning" role="group">
              <template v-for="num in 5">
              <input type="radio" class="btn-check" :name="'rating' + num" :id="'rating' + num" :value="num" v-model="rating">
              <label class="btn btn-outline-primary btn-sm " :for="'rating' + num">{{ num }}</label>
              </template>
              <button class="btn btn-outline-primary btn-sm btn-outline-danger " @click="rating = null">Clear</button>
            </div>
            
          </li>

        </ul>
      </div>
    
    </div>

  </template>
  
<script setup>
  import { ref, onMounted } from 'vue';
  import Dropdown from '@/components/Dropdown.vue';
  import axios from 'axios';
  
  const sections = ref([]);
  const authors = ref([]);
  const rating = ref(null);


  onMounted(async () => {
    try {
      const response = await axios.get('sections/all');
      sections.value = response.data.sections;
    } catch (error) {
      console.error(error);
    }

    try {
      const response = await axios.get('books/authors/all');
      authors.value = response.data.authors;
    } catch (error) {
      console.error(error);
    }

  });
</script>
  
<style scoped>

.btn-group .btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem; 
}

.card {
  width: 300px; /* Fixed width */
  border: 1px solid #ccc; /* Just for visual clarity */
  padding: 1px;

  display: flex; /* New */
  flex-direction: column; /* New */
  justify-content: space-between; /* New */
}

.card-body {
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Distributes space equally */
  align-items: center; /* Centers items horizontally */
  flex-grow: 1; /* Allows the body to expand */
}
</style>