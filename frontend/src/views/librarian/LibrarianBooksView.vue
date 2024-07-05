<template>
    <div class="container">
        <table class="table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Author</th>
                    <th>Section</th>
                    <th>Copies</th>
                    <th>Issued</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="book in books" :key="book.id">
                    <td>{{ book.id }}</td>
                    <td>{{ book.name }}</td>
                    <td>{{ book.author }}</td>
                    <td>{{ book.section.name }}</td>
                    <td>{{ book.copies }}</td>
                    <td>{{ book.issued }}</td>
                    <td>
                        <router-link :to="`/librarian/book/${book.id}`" class="btn btn-warning">EDIT</router-link>
                    </td>
                </tr>
            </tbody>
        </table>


        <Pagination :currentPage="currentPage" :totalPages="totalPages" :startPage="startPage" :endPage="endPage" :fetchData="fetchBooks" />


    </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Pagination from '@/components/Pagination.vue';

const books = ref([]);
const totalPages = ref(0);
const currentPage = ref(1);
const perPage = 3;

const startPage = ref(1);
const endPage = ref(3);

const fetchBooks = async (page) => {
    try {
        const response = await axios.get(`books/all?page=${page}&per_page=${perPage}`);
        console.log(response.data);

        books.value = response.data.books;
        totalPages.value = response.data.pagination.pages;
        currentPage.value = response.data.pagination.page;

        if (currentPage.value > endPage.value) {
            startPage.value += 3;
            endPage.value = Math.min(endPage.value + 3, totalPages.value);
        } else if (currentPage.value < startPage.value) {
            startPage.value -= 3;
            endPage.value = Math.min(endPage.value, currentPage.value);
        }
    } catch (error) {
        console.error(error);
    }
};

onMounted(async () => {
   await fetchBooks(currentPage.value);
});
</script>

<style scoped>


.container {
  display: flex;
  flex-direction: column;
  height: 85vh;
  justify-content: space-between;
}

</style>