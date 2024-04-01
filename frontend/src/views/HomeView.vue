<template>
  <div class="home">
    <div class="container">
      <h1>Books</h1>
      <div class="row">
        <div class="col-sm-12">
            <Book v-for="book in books" :key="book.id" :book="book" />
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
import { useStore } from 'vuex';

const books = ref([]);
const router = useRouter();
const store = useStore();


console.log(store.getters.userBooks);

onMounted(async () => {
  try {
    const response = await axios.get('books/all');
    books.value = response.data.books;
  } catch (error) {
      console.log('Error:', error);
  }
  
});
</script>