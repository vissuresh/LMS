<template>
  <div class="card p-3">
    <div class="row">
      <div class="col-6 d-flex flex-column justify-content-between">

        <div class="card-title">
          <h5 class="truncate">{{ book.name }}</h5>
          <span class="card-subtitle text-muted truncate">by {{ book.author }}</span>
        </div>


        <div>
          <span v-if="book.section" class="truncate">Section: 
            <router-link :to="{name: 'BooksView', query: {section_id: book.section.id}}">
              {{ book.section.name }}
            </router-link>
          </span>
          <span v-else class="truncate">Section: Unspecified</span>
        </div>

        <div>
          <button type="button" class="btn btn-primary" @click="requestBook(book.id)">Request</button>
        </div>
        
        <div>
          <button class="btn btn-warning"><router-link :to="`/books/${book.id}`">View More</router-link></button>
        </div>

      </div>

      <div class="col">
        <img v-if="book.picture" :src="'data:image/jpeg;base64,' + book.picture" class="card-img-top" alt="Book picture">
        <img v-else src="/img/noPicture.jpg" class="card-img-top img-fluid" alt="No picture">
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, onMounted, watch } from 'vue';
import { createInfoModal } from '@/services/modal';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();


const props = defineProps({
  book: {
    type: Object,
    default: () => ({})
  }
});

const { book } = props;

const requestBook = async (bookId) => {
    let modal = null;

    try {
        const response = await axios.post(`/requests/${bookId}`);
        modal = createInfoModal('Success', 'Request successful!');

    } catch (error) {
        modal = createInfoModal('Error', error.response.data.message);
    }
    modal.show();
}


onMounted(() => {
    var myModalEl = document.getElementById('infoModal');
    if (myModalEl) {
        myModalEl.addEventListener('hidden.bs.modal', function (event) {
              window.location.reload();
        });
    }
});
</script>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  justify-content: space-evenly; 
  margin-bottom: 1em;
  height: 25vh;
  overflow: hidden;
}

.row{
  margin-bottom: 0 !important;
}

.card-img-top {
  height: 22vh;
}

.btn{
  width: 7  0%;
}


.truncate {
  white-space: normal; 
  overflow: hidden; 
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}
</style>