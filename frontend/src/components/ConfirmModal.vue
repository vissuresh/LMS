<template>
  <div class="modal fade" id="confirmModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="modalLabel">{{ title }}</h1>
        </div>  
        <div class="modal-body">{{ message }}</div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="emit('cancelled')" >Cancel</button>
          <button type="button" class="btn btn-primary" @click="emit('confirmed')">Confirm</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, onMounted, watch } from 'vue';
import { Modal } from 'bootstrap';

const props = defineProps({
  title: String,
  message: String,
  showModal: Boolean,
});

const emit = defineEmits(["confirmed", "cancelled"]);

let modalInstance = null;

onMounted(() => {
  const modalElement = document.getElementById('confirmModal');
  modalInstance = new Modal(modalElement);
});

watch(() => props.showModal, (newVal) => {
  if (newVal && modalInstance) {
    modalInstance.show();
  } else if (modalInstance) {
    modalInstance.hide();
  }
});
</script>