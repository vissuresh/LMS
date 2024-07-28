<template>
    <CommentModal :showModal="showModal" @submitComment="submitComment" @cancelComment="cancelComment" />
    <div class="card mb-4">
      <div class="row g-0">
        <div class="col-md-4">
          <img v-if="book.picture" :src="'data:image/jpeg;base64,' + book.picture" class="card-img-top img-fluid book-image rounded-start" alt="Book picture">
          <img v-else src="/img/noPicture.jpg" class="card-img-top img-fluid book-image rounded-start" alt="No picture">
        </div>
        <div class="col-md-8">
          <div class="card-body">
            <h5 class="card-title">
              <router-link :to="{name: 'BookView', params: {id: book.id}}">
                {{ book.name }}
              </router-link>
            </h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ book.author }}</h6>
            <div class="d-flex align-items-center mb-3">
              <span class="badge bg-success me-2">{{ book.rating }}</span>
              <div class="text-warning">
                <i v-for="n in 5" :key="n" :class="n <= book.rating ? 'bi bi-star-fill' : n <= Math.ceil(book.rating) ? 'bi bi-star-half' : 'bi bi-star'"></i>
              </div>
            </div>
            <h6 v-if="book.section" class="card-subtitle mb-2">Section: <router-link :to="{name: 'BooksView', query: {section_id: book.section.id}}">
              {{ book.section.name }}
            </router-link></h6>
            <h6 v-else>Unspecified</h6>
            
            <div v-if="requested" class="row justify-content-end">
              <div class="col-auto">
                <button class="btn btn-danger" @click="handleDeleteRequest">Delete Request</button>
              </div>
            </div>
            
            <div v-else-if="issued" class="row justify-content-end">
              <div class="col-auto">
                <button class="btn btn-primary" @click="handleReadBook">Read Book</button>
              </div>
              <div class="col-auto">
                <button class="btn btn-success" @click="handleAddComment">Add Feedback</button>
              </div>
              <div class="col-auto">
                <button class="btn btn-danger" @click="handleReturnBook">Return Book</button>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </template>
  
<script setup>
import { defineProps, onMounted, ref } from 'vue';
import { createInfoModal } from '@/services/modal';
import CommentModal from '@/components/CommentModal.vue';
import axios from 'axios';
import 'bootstrap-icons/font/bootstrap-icons.css';


const props = defineProps({
    book: {
        type: Object,
        required: true
    },
    issued: {
        type: Boolean,
        required: false
    },
    requested: {
        type: Boolean,
        required: false
    },
    requestId: {
        type: Number,
        required: false
    },

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
    const response = await axios.post(`/books/${props.book.id}/comments`, data);
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

  if(props.issued === true) {
    try {
        const response = await axios.delete(`/issues/return/${props.book.id}`);
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

const handleDeleteRequest = async () => {
  let modal = null;

    try {
        const response = await axios.delete(`/requests/${props.requestId}`);
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
  