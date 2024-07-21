<!-- src/components/CommentCard.vue -->
<template>
    <div class="card mb-3">
      <div class="card-body">
        <div class="d-flex">
          <div class="flex-shrink-0">
            <img :src="`https://placehold.co/50x50?text=${comment.rating}`" class="rounded-circle" :alt="`Rating ${comment.rating}`">
          </div>
          <div class="flex-grow-1 ms-3">
            <h6 class="fw-bold mb-1">{{ comment.user }}</h6>
            <p class="mb-0">{{ comment.comment }}</p>
            <small class="text-muted">Posted on {{ new Date(comment.date_created).toLocaleDateString() }}</small>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ['comment']
  };
  </script>
  