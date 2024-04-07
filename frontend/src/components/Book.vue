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
            <button type="button" class="btn btn-primary" @click="handleRequestBook">Request</button>
          </p>
          <p class="card-text">
            <button class="btn btn-warning">
              <router-link :to="`/books/${book.id}`">View More</router-link>
            </button>
          </p>
        </div>  
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
</style>