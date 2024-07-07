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
import { defineProps } from 'vue';
import { ref } from 'vue';

const props = defineProps({
  currentPage: Number,
  totalPages: Number,
  fetchData: Function
});

const startPage = ref(1);
const endPage = ref(0);
endPage.value = Math.min(3, props.totalPages);

if (props.currentPage > props.endPage) {
    props.startPage += 3;
    props.endPage = Math.min(props.endPage + 3, props.totalPages);
} else if (props.currentPage < props.startPage) {
    props.startPage -= 3;
    props.endPage = Math.min(props.endPage, props.currentPage);
}
</script>


<style scoped>
.page-link {
  cursor: pointer;
}
</style>