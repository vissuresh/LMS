<template>
  <div class="home">
    <div class="container">
      <h1 class="mb-5">Books</h1>
      <div class="row g-4">
        <div class="col-6" v-for="book in books" :key="book.id">
            <Book :book="book"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Book from '@/components/Book.vue';
import { useRouter } from 'vue-router';

const books = ref([]);
const router = useRouter();

onMounted(async () => {
  try {
    const response = await axios.get('books/all');
    books.value = response.data.books;
  } catch (error) {
      console.log('Error:', error);
  }
  
});
</script>