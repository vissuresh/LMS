<template>
    <Loading :isLoading="isLoading" />
    <div class="container my-5">
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">My Books</h5>
                        <!-- Add content for My Books card here -->
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Book Requests</h5>
                        
                    </div>
                </div>
            </div>
        </div>
    </div>
  </template>
  
<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import SectionCard from '@/components/SectionCard.vue';
import Loading from '@/components/Loading.vue';
import Pagination from '@/components/Pagination.vue';
import { createInfoModal } from '@/services/modal';

const sections = ref([]);
const totalPages = ref(0);
const currentPage = ref(1);
const isLoading = ref(false);

const searchQuery = ref('');

const fetchSections = async (page) => {
    isLoading.value = true;
    let modal = null;
    
    try {
        const queryParams = new URLSearchParams({
            query: searchQuery.value,
        });
        const response = await axios.get(`/sections/all?page=${page}&per_page=7&${queryParams}`);

        sections.value = response.data.sections;
        isLoading.value = false;

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

onMounted(() => {
    fetchSections(1);
});

</script>
  