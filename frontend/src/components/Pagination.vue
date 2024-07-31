<template>
    <nav class="pagination-container">
        <ul class="pagination justify-content-center">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <a class="page-link" @click="fetchData(currentPage - 1)" :disabled="currentPage === 1">Previous</a>
            </li>
            <li class="page-item" v-for="page in Array.from({length: endPage - startPage+ 1}, (_, i) => startPage + i)" :key="page" :class="{ active: currentPage === page }">
                <a class="page-link" @click="fetchData(page)">{{ page }}</a>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <a class="page-link" @click="fetchData(currentPage + 1)" :disabled="currentPage === totalPages">Next</a>
            </li>
        </ul>
    </nav>
</template>




<script setup>
import { defineProps, onMounted, ref, watch } from 'vue';

const props = defineProps({
  currentPage: Number,
  totalPages: Number,
  fetchData: Function
});

const startPage = ref(1);
const endPage = ref(0);
endPage.value = Math.min(3, props.totalPages);


const updatePages = () => {
  endPage.value = Math.min(3, props.totalPages);

  if (props.currentPage > endPage.value) {
    startPage.value += 3;
    endPage.value = Math.min(endPage.value + 3, props.totalPages);
  } else if (props.currentPage < startPage.value) {
    startPage.value -= 3;
    endPage.value = Math.min(endPage.value, props.currentPage);
  }
};

onMounted(() => {
  updatePages();
});


watch(
  () => props.totalPages,
  () => {
    updatePages();
  }
);
</script>


<style scoped>
.page-link {
  cursor: pointer;
}
</style>