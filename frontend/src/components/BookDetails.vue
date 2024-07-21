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
            <button class="btn btn-primary" @click="requestBook">Request Book</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
<script setup>
    import { defineProps } from 'vue';
    import 'bootstrap-icons/font/bootstrap-icons.css';

    const props = defineProps({
        book: {
            type: Object,
            required: true
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
  