<template>
    <Loading :isLoading="isLoading" />
    <div class="container-fluid my-5">
        <div class="row">
            <div class="col-6 mb-5">
                <div class="card px-4">
                    <div class="card-body">
                        <h2 class="card-title mb-5">My Books</h2>
                        <div class="row g-3" v-if="userIssues.length > 0" v-for="book in userIssues" :key="book.id">
                            <ProfileBook :book="book" :issued="true"/>
                        </div>
                        <div v-else>
                            <p>No books issued.</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-6">
                <div class="card px-4">
                    <div class="card-body">
                        <h2 class="card-title mb-5">Book Requests</h2>
                        <div class="row g-3" v-if="userRequests.length > 0" v-for="entry in userRequests" :key="entry.request_id">
                            <ProfileBook :book="entry.book" :requestId="entry.request_id" :requested="true"/>
                        </div>
                        <div v-else>
                            <p>No requests found.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
  </template>
  
<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Loading from '@/components/Loading.vue';
import { createInfoModal } from '@/services/modal';
import ProfileBook from '@/components/ProfileBook.vue';

const userIssues = ref([]);
const userRequests = ref([]);
const isLoading = ref(false);

const fetchBooks = async () => {
    isLoading.value = true;
    let modal = null;
    
    try {
        const response = await axios.get(`/books/user`);
        userIssues.value = response.data;

        const response1 = await axios.get(`/requests/user`);
        userRequests.value = response1.data;

        isLoading.value = false;
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

onMounted(() => {
    fetchBooks();
});

</script>

<style scoped>
.container-fluid {
    width: 90vw;
}
</style>

  