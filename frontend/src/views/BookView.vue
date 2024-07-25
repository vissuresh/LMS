<!-- src/views/BookView.vue -->
<template>
    <div class="container mt-5">
      <BookDetails :book="book"/>
      
      <hr class="my-4" />

      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <span>Comments</span>
          <div>
            <button class="btn btn-outline-primary btn-sm" @click="toggleSort">{{ sortByNewest ? 'Sort by Newest' : 'Sort by Rating' }}</button>
          </div>
        </div>
        <div class="card-body">
          <CommentCard v-for="comment in comments" :key="comment.id" :comment="comment" />
        </div>
      </div>
    </div>
  </template>
  
<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import BookDetails  from '@/components/BookDetails.vue';
import CommentCard from '@/components/CommentCard.vue';
import { useRoute } from 'vue-router';

const book = ref({});
const comments = ref([]);
const sortByNewest = ref(true);

const route = useRoute();
const bookId = route.params.id;


onMounted(async () => {
  try{
      const response = await axios.get(`books/${bookId}`);
      book.value = response.data;
  } catch(error) {
      console.error(error);
  }
  
  try {       
      const commentsResponse = await axios.get(`books/${bookId}/comments`);
      comments.value = commentsResponse.data;
  } catch (error) {
      console.error(error);
  }
});


const toggleSort = () => {
    sortByNewest.value = !sortByNewest.value;

    if (sortByNewest.value) {
        comments.value.sort((a, b) => new Date(b.date_created) - new Date(a.date_created));
    } else {
        comments.value.sort((a, b) => b.rating - a.rating);
    }
};

    

</script>