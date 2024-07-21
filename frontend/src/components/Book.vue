<template>
  <div class="card p-3">
    <div class="row">

      <div class="col-7">
        <div class="card-title">
          <div class="row">
            <div class="col-3">
              <h5>{{ book.name }}</h5>
            </div>
          </div>
          <h6 class="card-subtitle mb-4 text-muted">by {{ book.author }}</h6>

          <div class="row mb-4">
            <span v-if="book.section">Section:<router-link :to="`/sections/${book.section.id}`">{{ book.section.name }}</router-link></span>
            <span v-else >Section: Unspecified</span>
          </div>
        </div>

        <div class="row">
          <div class="col-6 p-1">
            <div class="card-body">
              <p class="card-text  text-start">
                <button type="button" class="btn btn-primary" @click="handleRequestBook">Request</button>
              </p>
              <p class="card-text  text-start">
                <button class="btn btn-warning">
                  <router-link :to="`/books/${book.id}`">View More</router-link>
                </button>
              </p>
            </div>
          </div>
        </div>
        
      </div>

      <div class="col limited-height">
        <img v-if="book.picture" :src="'data:image/jpeg;base64,' + book.picture" class="card-img-top" alt="Book picture">
        <img v-else src="/img/noPicture.jpg" class="card-img-top img-fluid" alt="No picture">
      </div>

    </div>
  </div>

</template>
  
<script setup>
import { requestBook } from '@/services/requestBook.js';


const props = defineProps({
  book: {
    type: Object,
    default: () => ({})
  }
});

const { book } = props;

const handleRequestBook = () => requestBook(book.id);
</script>

<style scoped>
.card {
  margin-bottom: 1em;
}

.limited-height {
  max-height: 25vh; /* Example height */
  overflow: hidden; /* Ensures content exceeding the height is not visible */
}

.card-img-top {
  width: 100%; /* Makes image responsive */
  height: 100%; /* Image will take up the full height of the container */
  object-fit:cover /* Adjust as needed */
}
</style>