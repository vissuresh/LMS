<template>

    <div class="card text-center">
      <div class="card-header">
        Select Filters
      </div>
      <div class="card-body">
        <ul class="list-group list-group-flush">

          <li class="list-group-item mb-5">
            <h5 class="card-title">Sections</h5>
            <Dropdown :options="sections" :title="'Sections'" @updateValue="handleSectionsEvent" />
          </li>

          <li class="list-group-item mb-5">
            <h5 class="card-title">Authors</h5>
            <Dropdown :options="authors" :title="'Authors'" @updateValue="handleAuthorsEvent" />
          </li>

          <li class="list-group-item ">
            <h5 class="card-title">Rating</h5>
            <Rating @updateValue="handleRatingEvent" />
          </li>

        </ul>
      </div>

      <div class="card-footer">
        <button class="btn btn-primary btn-sm" @click="applyFilters" >Apply Filters</button>
      </div>
    
    </div>

  </template>
  
<script setup>
  import { ref, onMounted } from 'vue';
  import Dropdown from '@/components/Dropdown.vue';
  import Rating from '@/components/Rating.vue';
  import axios from 'axios';
  import { useStore } from 'vuex';
  import { createInfoModal } from '@/services/modal';

  const store = useStore();

  const sections = ref([]);
  const authors = ref([]);

  const selectedSections = ref([]);
  const selectedAuthors = ref([]);
  const selectedRating = ref(0);

  const handleSectionsEvent = (sections) => {
    selectedSections.value = sections.value;
  };

  const handleAuthorsEvent = (authors) => {
    selectedAuthors.value = authors.value;
  };

  const handleRatingEvent = (rating) => {
    selectedRating.value = rating;
  };

  const applyFilters = () => {
    store.dispatch('setFilters', {
      sections: selectedSections.value,
      authors: selectedAuthors.value,
      rating: selectedRating.value
    });

    createInfoModal('Filters', 'Filters have been applied.').show();
  };


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
  width: 15vw;
  height: 80vh;
  overflow-y: auto;

  display: flex; /* New */
  flex-direction: column; /* New */
  justify-content: space-between; /* New */
}

.card-body {
  display: flex;
  flex-direction: column;
  justify-content: center; /* Distributes space equally */
  align-items: center; /* Centers items horizontally */
  flex-grow: 1; /* Allows the body to expand */
}
</style>