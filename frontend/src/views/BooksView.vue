<template>
  <Loading :isLoading="isLoading" />
  <div class="container-fluid">
    <div class="row">
      <div class="col-2"><FilterSidebar @apply-filters="handleApplyFilters" class="mr-5"/></div>

      <div class="col">

        <div class="row mb-2">

          <div class="col-5">
            <h1>Books</h1>
          </div>

          <div class="col-6">
              <div class="input-group">
                  <div class="dropdown">
                      <button class="btn btn-outline-secondary dropdown-toggle" type="button" @click="dropdownOpen = !dropdownOpen">
                      {{ search_by === 'book_name' ? 'Book Name' : 'Book ID' }}
                      </button>
                      <ul class="dropdown-menu" :class="{ show: dropdownOpen }">
                          <li><a class="dropdown-item clickable" @click="selectOption('book_name')">Book Name</a></li>
                          <li><a class="dropdown-item clickable" @click="selectOption('book_id')">Book ID</a></li>
                      </ul>
                  </div>
                  <input type="text" class="form-control" v-model="searchQuery" placeholder="Search books..." />
              </div>
          </div>

          <div class="col-1">
              <button class="btn btn-outline-primary" @click="fetchBooks(1)">Search</button>
          </div>

        </div>


        <div class="row g-3">
          <div class="col-3" v-for="book in books" :key="book.id">
              <Book :book="book"/>
          </div>
        </div>

        <div v-if="totalPages > 0">
          <Pagination :currentPage="currentPage" :totalPages="totalPages" :fetchData="fetchBooks" />
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import Book from '@/components/Book.vue';
import FilterSidebar from '@/components/FilterSidebar.vue';
import Loading from '@/components/Loading.vue';
import { createInfoModal } from '@/services/modal';
import Pagination from '@/components/Pagination.vue';

const route = useRoute();

const books = ref([]);
const totalPages = ref(0);
const currentPage = ref(1);

const isLoading = ref(false);

const searchQuery = ref('');
const selectedSectionIds = ref([]);
const selectedAuthors = ref([]);
const selectedRating = ref(0);

const dropdownOpen = ref(false);
const search_by = ref('book_name');

const selectOption = (option) => {
    search_by.value = option;
    dropdownOpen.value = false;
};

const handleApplyFilters = (filters) => {
  selectedSectionIds.value = filters.section_ids;
  selectedAuthors.value = filters.authors;
  selectedRating.value = filters.rating;

  console.log('Applied Filters:', filters);
};

const fetchBooks = async (page) => {
    isLoading.value = true;
    let modal = null;

    try {
        const queryParams = new URLSearchParams({
                query: searchQuery.value,
                search_by: search_by.value,
                sections: selectedSectionIds.value,
                authors: selectedAuthors.value.map(author => author.name),
                rating: selectedRating.value
            }).toString();

        const response = await axios.get(`books/all?page=${page}&per_page=12&${queryParams}`);
        isLoading.value = false;

        books.value = response.data.books;
        totalPages.value = response.data.pagination.pages;
        currentPage.value = response.data.pagination.page;


    } catch (error) {
        console.error(error);
        if(error.response && error.response.data){
            modal = createInfoModal("Error", error.response.data.message);
        } else{
            modal = createInfoModal("Error", "An error occurred.");
        }
        isLoading.value = false;
        modal.show();
    }
    
};


watch(
  () => route.query,
  (newQuery) => {
    if (newQuery.section_id) {
      selectedSectionIds.value = [newQuery.section_id];
      fetchBooks(1);
    } else {
      selectedSectionIds.value = [];
      fetchBooks(1);
    }
  },
  { immediate: true }
);


onMounted(async () => {
  if(route.query && route.query.section_id){
    selectedSectionIds.value = [route.query.section_id];
  }
  await fetchBooks(currentPage.value);
  
});

</script>

<style scoped>
.container-fluid {
    width: 97vw;
}
</style>