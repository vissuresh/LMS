<template>
    <div class="container custom-container">
        <div class="d-flex">
            <FilterSidebar class="mr-5"/>

            <div class="content-wrapper flex-grow-1">

                <div class="row mb-5">
                    <div class="col">
                        <input type="text" class="form-control" v-model="searchQuery" placeholder="Search books..." />
                    </div>
                    <div class="col">
                        <button class="btn btn-outline-secondary" @click="searchBooks">Search</button>
                    </div>
                </div>

                <div class="flex-column-container">
                    <table class="table table-striped">
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
                </div>
                

                <div class="pagination-container">
                    <Pagination :currentPage="currentPage" :totalPages="totalPages" :fetchData="fetchBooks" />
                </div>

            </div>
        </div>
    </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Pagination from '@/components/Pagination.vue';
import FilterSidebar from '@/components/FilterSidebar.vue';

const books = ref([]);
const totalPages = ref(0);
const currentPage = ref(1);

const fetchBooks = async (page) => {
    try {
        const response = await axios.get(`books/all?page=${page}&per_page=10`);

        books.value = response.data.books;
        totalPages.value = response.data.pagination.pages;
        currentPage.value = response.data.pagination.page;

    } catch (error) {
        console.error(error);
    }
};




const searchBooks = async () => {
    if (searchQuery.value.trim()) {
        try {
            const response = await axios.get(`/books/search?query=${encodeURIComponent(searchQuery.value)}`);
            books.value = response.data;
            // Reset pagination if necessary
        } catch (error) {
            console.error("Failed to search books:", error);
        }
    }
};




onMounted(async () => {
   await fetchBooks(currentPage.value);
});
</script>

<style scoped>

.custom-container {
  max-width: 90%; /* Adjust this value as needed */
  margin-right: auto;
  margin-left: auto;
}

.flex-column-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.content-wrapper {
  margin-left: 20px; /* Adjust the space as needed */
}


.content-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* This will push the pagination to the bottom */
  height: 100%; /* Ensure it takes full height */
}
</style>