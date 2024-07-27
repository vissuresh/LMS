2<template>
    <div class="card mb-4">
      <div class="row g-0">
        <div class="col-md-4">
          <img v-if="book.picture" :src="'data:image/jpeg;base64,' + book.picture" class="card-img-top img-fluid book-image rounded-start" alt="Book picture">
          <img v-else src="/img/noPicture.jpg" class="card-img-top img-fluid book-image rounded-start" alt="No picture">
        </div>
        <div class="col-md-8">
          <div class="card-body">
            <h5 class="card-title">{{ book.name }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ book.author }}</h6>
            <h6 v-if="book.section" class="card-subtitle mb-2">Section: <router-link :to="{name: 'BooksView', query: {section_id: book.section.id}}">
              {{ book.section.name }}
            </router-link></h6>
            <h6 v-else>Unspecified</h6>
            <button v-if="bookRequestedByUser" class="btn btn-danger" @click="handleDeleteRequest">Delete Request</button>
            <div class="row justify-content-end">
              <div class="col-auto">
                <button v-if="issued" class="btn btn-primary" @click="handleReadBook">Read Book</button>
                <button v-else class=""></button>
              </div>
            </div>

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
    },
    issued: Boolean,
});


const showModal = ref(false);

const handleAddComment = () => {
  showModal.value = true;
};

const submitComment = async (data) => {
  showModal.value = false;
  let modal = null;

  let comment = data.comment;
  let rating = data.rating;

  if (!comment || comment.trim() === '' || !rating || rating < 1 || rating > 5) {
    cancelComment();
    return;
  }
  

  try {
    const response = await axios.post(`/books/${bookId}/comments`, data);
    modal = createInfoModal('Comment', 'Comment added successfully!');
  } catch (error) {
    if(error.response && error.response.data){
      modal = createInfoModal('Comment', error.response.data.message);
    } else {
      modal = createInfoModal('Comment', 'An error occurred.');
    } 
  }
  modal.show();
};

const cancelComment = () => {
  showModal.value = false;
}

const handleReturnBook = async () => {
  let modal = null;

  if(bookIssuedToUser.value === true) {
    try {
        const response = await axios.delete(`/issues/return/${bookId}`);
        bookIssuedToUser.value = false;
        modal = createInfoModal('Return', 'Book returned successfully!');

    } catch (error) {
        if(error.response && error.response.data){
          modal = createInfoModal('Book Return', error.response.data.message);
        } else {
          modal = createInfoModal('Book Return', 'An error occurred.');
        } 
    }
    modal.show();
  }

    
};

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
  } catch (error) {
    console.error(error);
  }

  try {
    const response = await axios.get('requests/user');
    userRequests.value = response.data;
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
  