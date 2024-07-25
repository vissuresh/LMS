<template>
    <ConfirmModal :showModal="showModal" :title="`Delete Book`" :message="confirmModalMessage" @confirmed="onConfirmed" @cancelled="onCancelled" />
    <Loading :isLoading="isLoading" />
    <div class="container-fluid  custom-container">
        <div class="d-flex">
            <FilterSidebar class="mr-5"/>

            <div class="content-wrapper flex-grow-1">

                <div class="row mb-5">
                    <div class="col-5">
                        <router-link :to="{ name: 'LibrarianBookAdd' }" class="btn btn-primary">Add Book</router-link>
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
                

                <div class="flex-column-container">
                    <table class="table table-striped table-hover text-center">
                    <thead class="table-dark">
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Author</th>
                            <th>Section</th>
                            <th>Copies</th>
                            <th>Issued</th>
                            <th colspan="2" class="border-start">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="table-group-divider">
                        <tr v-for="book in books" :key="book.id">
                            <td>{{ book.id }}</td>
                            <td>{{ book.name }}</td>
                            <td>{{ book.author }}</td>
                            <td>{{ book.section ? book.section.name : 'NULL' }}</td>
                            <td>{{ book.copies }}</td>
                            <td>{{ book.issued }}</td>
                            <td class="border-start"><router-link :to="{ name: 'LibrarianBookEdit', params: {bookId : book.id} }" class="btn btn-warning">EDIT</router-link></td>
                            <td><button class="btn btn-danger" @click="deleteBook(book)">DELETE</button></td>
                        </tr>
                    </tbody>
                    </table>
                </div>
                

                <div v-if="totalPages > 0">
                    <Pagination :currentPage="currentPage" :totalPages="totalPages" :fetchData="fetchBooks" />
                </div>

            </div>
        </div>
    </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import Pagination from '@/components/Pagination.vue';
import FilterSidebar from '@/components/FilterSidebar.vue';
import { createInfoModal } from '@/services/modal';
import ConfirmModal from '@/components/ConfirmModal.vue';
import Loading from '@/components/Loading.vue';

const store = useStore();
const showModal = ref(false);
const currentBookIdToDelete = ref(null);
const confirmModalMessage = ref('Are you sure you want to delete this book? ');
const isLoading = ref(false);

const books = ref([]);
const totalPages = ref(0);
const currentPage = ref(1);

const searchQuery = ref('');
const selectedSections = computed(() => store.getters.selectedSections);
const selectedAuthors = computed(() => store.getters.selectedAuthors);
const selectedRating = computed(() => store.getters.selectedRating);

const dropdownOpen = ref(false);
const search_by = ref('book_name');

const selectOption = (option) => {
    search_by.value = option;
    dropdownOpen.value = false;
};

const fetchBooks = async (page) => {
    isLoading.value = true;
    let modal = null;
    try {
        const queryParams = new URLSearchParams({
                query: searchQuery.value,
                search_by: search_by.value,
                sections: selectedSections.value.map(section => section.id),
                authors: selectedAuthors.value.map(author => author.name),
                rating: selectedRating.value
            }).toString();

        const response = await axios.get(`books/all?page=${page}&per_page=11&${queryParams}`);
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


const deleteBook = (book) => {
    currentBookIdToDelete.value = book.id;
    confirmModalMessage.value = `Are you sure you want to delete the book <ID: ${book.id}, Name: ${book.name} >"?`;
    showModal.value = true;
};


const onConfirmed = async () => {
    showModal.value = false;
    isLoading.value = true;
    let modal = null;

    try {
        await axios.delete(`books/${currentBookIdToDelete.value}`);
        modal = createInfoModal("Success", "Book deleted successfully.");
    } catch (error) {
        console.error(error);

        if(error.response && error.response.data){
            modal = createInfoModal("Error", error.response.data.message);
        } else{
            modal = createInfoModal("Error", "An error occurred.");
        }
    }
    currentBookIdToDelete.value = null;
    isLoading.value = false;
    modal.show();

};

const onCancelled = () => {
    showModal.value = false;
    currentBookIdToDelete.value = null;
};



onMounted(async () => {
   await fetchBooks(currentPage.value);

   var confirmModal = document.getElementById('confirmModal');
    if (confirmModal) {
        confirmModal.addEventListener('hidden.bs.modal', function (event) {
            currentBookIdToDelete.value = null;
        });
    }

    var infoModal = document.getElementById('infoModal');
    if (infoModal) {
        infoModal.addEventListener('hidden.bs.modal', function (event) {
            window.location.reload();
        });
    }

});
</script>

<style scoped>

.clickable { 
    cursor: pointer;
}

.custom-container {
  max-width: 90%;
  margin-right: auto;
  margin-left: auto;
}

.flex-column-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.content-wrapper {
  margin-left: 2%;
}


.content-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 80vh;
}
</style>