<template>
  <div class="container">
    <h1 class="mb-5">Books</h1>
    <div class="row g-3">
      <div class="col-4" v-for="book in books" :key="book.id">
          <Book :book="book"/>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Book from '@/components/Book.vue';

const books = ref([]);

onMounted(async () => {
  try {
    const response = await axios.get('books/all');
    books.value = response.data.books;
  } catch (error) {
      console.log('Error:', error);
  }
  
});
</script>