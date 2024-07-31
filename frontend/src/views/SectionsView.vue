<template>
    <Loading :isLoading="isLoading" />
    <div class="container mt-5">
        <div class="row mb-5">

            <div class="col-5">
                <h1>Sections</h1>
            </div>

            <div class="col-6">
                <div class="input-group">
                    <input type="text" class="form-control" v-model="searchQuery" placeholder="Search sections..." />
                </div>
            </div>

            <div class="col-1">
                <button class="btn btn-outline-primary" @click="fetchSections(1)">Search</button>
            </div>

        </div>

        <SectionCard v-for="section in sections" :key="section.name" :section="section" />

        <div v-if="totalPages > 0">
            <Pagination :currentPage="currentPage" :totalPages="totalPages" :fetchData="fetchSections" />
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
        if(error.response && error.response.data && error.response.data.message){
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
  