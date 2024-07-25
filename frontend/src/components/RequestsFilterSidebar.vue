<template>

    <div class="card text-center">
      <div class="card-header">
        Select Filters
      </div>
      <div class="card-body">
        <ul class="list-group list-group-flush">

          <li class="list-group-item mb-5">
            <h5 class="card-title">User</h5>
            <input type="text" v-model="userEmail" class="form-control" placeholder="User email">
          </li>

          <li class="list-group-item mb-5">
            <h5 class="card-title">Books</h5>
            <Dropdown :options="books" :title="'Books'" @updateValue="handleBooksEvent" />
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
  import axios from 'axios';
  import { useStore } from 'vuex';

  const store = useStore();

  const userEmail = ref('');
  const books = ref([]);
  const selectedBooks = ref([]);

  const handleBooksEvent = (books) => {
    selectedBooks.value = books.value;
  };

  const applyFilters = () => {
    store.dispatch('setBookRequestFilters', {
      userEmail: userEmail.value,
      books: selectedBooks.value,
    });

    alert('Filters have been applied.');
  };


  onMounted(async () => {
    try {
      const response = await axios.get('books/all/short');
      books.value = response.data;
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