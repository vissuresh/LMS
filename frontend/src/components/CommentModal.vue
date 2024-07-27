<template>
  <div class="modal fade" id="commentModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="modalLabel">Add your feedback</h1>
        </div>  
        <div class="modal-body">
            <div class="row">
              <label for="comment" class="form-label">Comment</label>
              <textarea  v-model="comment" class="form-control" placeholder="Enter your comment here..." required> </textarea>
            </div>

            <div class="row">
              <label for="rating" class="form-label">Rating</label>
              <input type="number" v-model="rating" class="form-control" placeholder="Enter your rating here..." min="1" max="5" step="0.1" required/>
            </div>
            
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="emit('cancelComment')" >Cancel</button>
          <button type="button" class="btn btn-primary" @click="submitComment">Confirm</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {  defineProps, onMounted, ref, watch, defineEmits } from 'vue';
import { Modal } from 'bootstrap';


const props = defineProps({
  showModal: Boolean,
});

const emit = defineEmits(["cancelComment", "submitComment"]); 

const comment = ref('');
const rating = ref(null);

const submitComment = () => {
  emit('submitComment', {comment: comment.value, rating: rating.value});
}

let modalInstance = null;

onMounted(() => {
  const modalElement = document.getElementById('commentModal');
  modalInstance = new Modal(modalElement);
});



watch(() => props.showModal, (newVal) => {
  if (newVal && modalInstance) {
    modalInstance.show();
  } else if (modalInstance) {
    comment.value = '';
    rating.value = null;
    modalInstance.hide();
  }
});
</script>