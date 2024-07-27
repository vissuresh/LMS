<!-- src/components/CommentCard.vue -->
<template>
    <div class="card mb-3">
      <div class="card-body">
        <div class="d-flex">
          <div :class="['number-badge', ratingClass]">
            {{ comment.rating }}
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
  import { computed } from 'vue';
  
  export default {
    props: ['comment'],
    setup(props) {
      const ratingClass = computed(() => {
        if (props.comment.rating <= 2) {
          return 'low';
        } else if (props.comment.rating <= 3) {
          return 'medium-low';
        } else if (props.comment.rating <= 4) {
          return 'medium-high';
        } else {
          return 'high';
        }
      });
  
      return {
        ratingClass
      };
    }
  };
  </script>


<style scoped>
.number-badge {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
}

.number-badge.low { background-color: #f8d7da; } 
.number-badge.medium-low { background-color: #ffe5b4; } 
.number-badge.medium-high { background-color: #f5f227; } 
.number-badge.high { background-color: #d4edda; }
</style>
  