<template>
  <div class="card col-6">
    <div class="card-body">
      
      <div class="row">

        <div class="col">
            <h5 class="card-title">{{ book.name }}</h5>
            <h6 class="card-subtitle mb-4 text-muted">by {{ book.author }}</h6>
            <p class="card-text">{{ book.desc ? book.desc.substring(0, 64) + '...' : '' }}</p>
        </div>

        <div class="col text-end">
          <p class="card-text mb-5">
            <router-link :to="`/section/${book.section.id}`">{{ book.section.name }}</router-link>
          </p>
          <p class="card-text">
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#requestModal">
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

  <Modal />
</template>
  
<script setup>
import { ref, toRefs } from 'vue';
import Modal from '@/components/Modal.vue';

const props = defineProps({
  book: {
    type: Object,
    default: () => ({})
  }
});

const { book } = toRefs(props);
</script>

<style scoped>
.card {
  margin-bottom: 1em;
}
</style>