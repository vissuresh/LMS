<template>
    <ConfirmModal :showModal="showModal" :title="`Delete Section`" :message="confirmModalMessage" @confirmed="onConfirmed" @cancelled="onCancelled" />
    <Loading :isLoading="isLoading" />
    <div class="container-fluid  custom-container">
        <div class="d-flex">

            <div class="content-wrapper flex-grow-1">

                <div class="row mb-5">
                    <div class="col-5">
                        <router-link :to="{ name: 'LibrarianSectionAdd' }" class="btn btn-primary">Add Section</router-link>
                    </div>

                    <div class="col-6">
                        <div class="input-group">
                            <div class="dropdown">
                                <button class="btn btn-outline-secondary dropdown-toggle" type="button" @click="dropdownOpen = !dropdownOpen">
                                {{ search_by === 'section_name' ? 'Section Name' : 'Section ID' }}
                                </button>
                                <ul class="dropdown-menu" :class="{ show: dropdownOpen }">
                                    <li><a class="dropdown-item clickable" @click="selectOption('section_name')">Section Name</a></li>
                                    <li><a class="dropdown-item clickable" @click="selectOption('section_id')">Section ID</a></li>
                                </ul>
                            </div>
                            <input type="text" class="form-control" v-model="searchQuery" placeholder="Search sections..." />
                        </div>
                    </div>

                    <div class="col-1">
                        <button class="btn btn-outline-primary" @click="fetchSections(1)">Search</button>
                    </div>

                </div>
                

                <div class="flex-column-container">
                    <table class="table table-striped table-hover text-center">
                    <thead class="table-dark">
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Description</th>
                            <th colspan="2" class="border-start">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="table-group-divider">
                        <tr v-for="section in sections" :key="section.id">
                            <td>{{ section.id }}</td>
                            <td>{{ section.name }}</td>
                            <td>{{ section.desc }}</td>
                            <td class="border-start"><router-link :to="{ name: 'LibrarianSectionEdit', params: {sectionId : section.id} }" class="btn btn-warning">EDIT</router-link></td>
                            <td><button class="btn btn-danger" @click="deleteSection(section)">DELETE</button></td>
                        </tr>
                    </tbody>
                    </table>
                </div>
                

                <div v-if="totalPages > 0">
                    <Pagination :currentPage="currentPage" :totalPages="totalPages" :fetchData="fetchSections" />
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
import { createInfoModal } from '@/services/modal';
import ConfirmModal from '@/components/ConfirmModal.vue';
import Loading from '@/components/Loading.vue';

const store = useStore();
const showModal = ref(false);
const currentSectionIdToDelete = ref(null);
const confirmModalMessage = ref('Are you sure you want to delete this section? ');
const isLoading = ref(false);

const sections = ref([]);
const totalPages = ref(0);
const currentPage = ref(1);

const searchQuery = ref('');

const dropdownOpen = ref(false);
const search_by = ref('section_name');

const selectOption = (option) => {
    search_by.value = option;
    dropdownOpen.value = false;
};

const fetchSections = async (page) => {
    isLoading.value = true;
    let modal = null;
    try {
        const queryParams = new URLSearchParams({
                query: searchQuery.value,
                search_by: search_by.value,
            }).toString();

        const response = await axios.get(`sections/all?page=${page}&per_page=11&${queryParams}`);
        isLoading.value = false;

        sections.value = response.data.sections;
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


const deleteSection = (section) => {
    currentSectionIdToDelete.value = section.id;
    confirmModalMessage.value = `Are you sure you want to delete the section <ID: ${section.id}, Name: ${section.name} >"?`;
    showModal.value = true;
};


const onConfirmed = async () => {
    console.log('Deleting section with ID:', currentSectionIdToDelete.value);
    showModal.value = false;
    isLoading.value = true;
    let modal = null;

    try {
        await axios.delete(`sections/${currentSectionIdToDelete.value}`);
        modal = createInfoModal("Success", "Section deleted successfully.");
    } catch (error) {
        console.error(error);

        if(error.response && error.response.data){
            modal = createInfoModal("Error", error.response.data.message);
        } else{
            modal = createInfoModal("Error", "An error occurred.");
        }
    }
    currentSectionIdToDelete.value = null;
    isLoading.value = false;
    modal.show();

};

const onCancelled = () => {
    showModal.value = false;
    currentSectionIdToDelete.value = null;
};



onMounted(async () => {
   await fetchSections(currentPage.value);

   var confirmModal = document.getElementById('confirmModal');
    if (confirmModal) {
        confirmModal.addEventListener('hidden.bs.modal', function (event) {
            currentSectionIdToDelete.value = null;
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