<!-- src/components/BookDetails.vue -->
<template>
    <div class="card mb-4">
      <div class="row g-0">
        <div class="col-md-4">
          <img v-if="book.picture" :src="'data:image/jpeg;base64,' + book.picture" class="card-img-top img-fluid book-image rounded-start" alt="Book picture">
          <img v-else src="/img/noPicture.jpg" class="card-img-top img-fluid rounded-start" alt="No picture">
        </div>
        <div class="col-md-8">
          <div class="card-body">
            <h5 class="card-title">{{ book.name }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ book.author }}</h6>
            <p class="card-text">{{ book.desc }}</p>
            <div class="d-flex align-items-center mb-3">
              <span class="badge bg-success me-2">{{ book.rating }}</span>
              <div class="text-warning">
                <i v-for="n in 5" :key="n" :class="n <= book.rating ? 'bi bi-star-fill' : n <= Math.ceil(book.rating) ? 'bi bi-star-half' : 'bi bi-star'"></i>
              </div>
            </div>
            <h6 class="card-subtitle mb-2">Section: {{ book.section ? book.section.name : "Unspecified"  }}</h6>
            <button v-if="bookRequestedByUser" class="btn btn-danger" @click="handleDeleteRequest">Delete Request</button>
            <button v-else-if="bookIssuedToUser" class="btn btn-success" @click="handleReadBook">Read Book</button>
            <button v-else class="btn btn-primary" @click="handleRequestBook">Request Book</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
<script setup>
import { defineProps, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { createInfoModal } from '@/services/modal';
import axios from 'axios';
import { saveToStorage, loadFromStorage } from '@/services/storage';
import 'bootstrap-icons/font/bootstrap-icons.css';

const route = useRoute();
const bookId = route.params.id;

const userBooks = ref([]);
const userRequests = ref([]);

const bookIssuedToUser = ref(null);
const bookRequestedByUser = ref(null);

const requestId = ref(null);
const issueId = ref(null);

const props = defineProps({
    book: {
        type: Object,
        required: true
    }
});

const handleRequestBook = async () => {
  let modal = null;

    try {
        const response = await axios.post(`/requests/${bookId}`);
        bookRequestedByUser.value = true;
        modal = createInfoModal('Request', 'Request successful!');

    } catch (error) {
        if(error.response && error.response.data){
          modal = createInfoModal('Request', error.response.data.message);
        } else {
          modal = createInfoModal('Request', 'An error occurred.');
        } 
    }
    modal.show();
};

const handleDeleteRequest = async () => {
  let modal = null;

    try {
        const response = await axios.delete(`/requests/${requestId.value}`);
        bookRequestedByUser.value = false;
        modal = createInfoModal('Request', 'Request deleted successfully!');

    } catch (error) {
        if(error.response && error.response.data){
          modal = createInfoModal('Request', error.response.data.message);
        } else {
          modal = createInfoModal('Request', 'An error occurred.');
        } 
    }
    modal.show();
};

onMounted(async () => {

  try {
    const response = await axios.get('books/user');
    userBooks.value = response.data;
    saveToStorage('userBooks', userBooks.value);
  } catch (error) {
    console.error(error);
  }

  try {
    const response = await axios.get('requests/user');
    userRequests.value = response.data;
    saveToStorage('userRequests', userRequests.value);
  } catch (error) {
    console.error(error);
  }



  for(let id of userBooks.value) {
    if(id.toString() === bookId) {
      bookIssuedToUser.value = true;
      break;
    }
  }
  for(let entry of userRequests.value) {
    let book_id = entry.book_id.toString();
    if(book_id === bookId) {
      bookRequestedByUser.value = true;
      requestId.value = entry.request_id;
      break;
    }
  }


  var myModalEl = document.getElementById('infoModal');
    if (myModalEl) {
        myModalEl.addEventListener('hidden.bs.modal', function (event) {
              window.location.reload();
        });
    }
});
</script>


<style scoped>
   .book-image {
      width: 100%;
      height: auto;
      max-width: 200px;
      object-fit: cover;
}</style>
  