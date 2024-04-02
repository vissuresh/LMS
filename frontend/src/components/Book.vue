<template>
  <div class="card h-100 d-inline-block w-100 p-3">
    <div class="card-body">
      <div class="row">
        <div class="col-8">
            <h5 class="card-title">{{ book.name }}</h5>
            <h6 class="card-subtitle mb-4 text-muted">by {{ book.author }}</h6>
            <p class="card-text">{{ book.desc ? book.desc.substring(0, 128) + '...' : '' }}</p>
        </div>

        <div class="col text-end">
          <p class="card-text mb-5">
            <router-link :to="`/section/${book.section.id}`">{{ book.section.name }}</router-link>
          </p>
          <p class="card-text">
            <button type="button" class="btn btn-primary" @click="requestBook">
              Request
            </button>
          </p>
          <p class="card-text">
            <button class="btn btn-warning">View More</button>
          </p>
        </div>
      </div>
    
    </div>
  </div>

  <ModalComponent />
</template>
  
<script setup>
import { ref } from 'vue';
import ModalComponent from '@/components/ModalComponent.vue';
import { useStore } from 'vuex';
import { Modal } from 'bootstrap';
import axios from 'axios';

const props = defineProps({
  book: {
    type: Object,
    default: () => ({})
  }
});

const { book } = props;
const vue_store = useStore();


const requestBook = async () => {

  const modalElement = document.getElementById('requestModal');
  const modal = new Modal(modalElement);
  const modalBody = document.querySelector('#requestModal .modal-body');

  if(vue_store.getters.userBooks.length + vue_store.getters.userRequests.length === 5){
    modalBody.textContent = 'You have reached the limit of 5 books';
    return modal.show();
  }

  for(let req of vue_store.getters.userRequests){
    if(req.book_id === book.id){
      modalBody.textContent = 'You have already requested this book';
      return modal.show();
    }
  }

  for(let user_book of vue_store.getters.userBooks){
    if(user_book.id === book.id){
      modalBody.textContent = 'You already have this book';
      return modal.show();
    }
  }

  try {
    const response = await axios.post(`/requests/${book.id}`);
    
    const newUserRequest = {
      "book_id": book.id,
      "request_id": response.data.request_id
    };

    vue_store.commit('addUserRequest', newUserRequest);
    modalBody.textContent = 'Request successful!';
  } catch (error) {
    console.log('Error:', error.response);
    modalBody.textContent = 'Request failed...';
  }
  modal.show();
}


</script>

<style scoped>
.card {
  margin-bottom: 1em;
}
</style>