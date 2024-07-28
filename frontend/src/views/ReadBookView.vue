<template>
    <Loading :isLoading="isLoading" />
    <div class="container-fluid book-reader-container h-100 d-flex justify-content-center align-items-center">
      <div class="reading-area">
        <iframe v-if="pdfUrl" :src="pdfUrl" class="w-100 h-100" frameborder="0"></iframe>
      </div>
    </div>
  </template>

  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRoute } from 'vue-router';
  import Loading from '@/components/Loading.vue';
  import { createInfoModal } from '@/services/modal';
  
  const pdfUrl = ref(null);
  const route = useRoute();
  const bookId = route.params.bookId;
  const isLoading = ref(false);
  
  onMounted(async () => {
    let modal = null;
    isLoading.value = true;
    try {
      const response = await axios.get(`/issues/read-book/${bookId}`, {
        responseType: 'blob',
      });
      const pdfBlob = new Blob([response.data], { type: 'application/pdf' });
      pdfUrl.value = URL.createObjectURL(pdfBlob);
    } catch (error) {
      console.error('Error loading PDF:', error);
      modal = createInfoModal('Error', 'Failed to load the PDF.');
    } finally {
      isLoading.value = false;
      if (modal) modal.show();
    }
  });
  </script>
  
  <style scoped>
.book-reader-container {
  height: 100vh;
}

.reading-area {
  width: 90vw;
  height: 90vh;
}

.reading-area iframe {
    border: none;
}
  </style>
  