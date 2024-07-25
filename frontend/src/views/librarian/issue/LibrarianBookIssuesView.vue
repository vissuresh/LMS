<template>
    <ConfirmModal :showModal="showModal" :title="`Revoke Issue`" :message="confirmModalMessage" @confirmed="onConfirmed" @cancelled="onCancelled" />
    <Loading :isLoading="isLoading" />
    <div class="container-fluid  custom-container">
        <div class="d-flex">
            <RequestsFilterSidebar class="mr-5"/>

            <div class="content-wrapper flex-grow-1">

                <div class="row mb-5">

                    <div class="col-3">
                        <div class="input-group">
                            <input type="text" class="form-control" v-model="searchQuery" placeholder="Search by Issue ID" />
                        </div>
                    </div>

                    <div class="col-1">
                        <button class="btn btn-outline-primary" @click="fetchIssues(1)">Search</button>
                    </div>

                </div>
                

                <div class="flex-column-container">
                    <table class="table table-striped table-hover text-center">
                    <thead class="table-dark">
                        <tr>
                            <th>Issue ID</th>
                            <th>User Email</th>
                            <th>Book ID</th>
                            <th>Book Name</th>
                            <th>Book Available</th>
                            <th colspan="1" class="border-start">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="table-group-divider">
                        <tr v-for="issue in issues" :key="issue.id">
                            <td>{{ issue.id }}</td>
                            <td>{{ issue.user.email }}</td>
                            <td>{{ issue.book.id }}</td>
                            <td>{{ issue.book.name }}</td>
                            <td>{{ issue.book.copies - issue.book.issued }}</td>
                            <td><button class="btn btn-danger" @click="revokeIssue(issue)">REVOKE</button></td>
                        </tr>
                    </tbody>
                    </table>
                </div>
                

                <div v-if="totalPages > 0">
                    <Pagination :currentPage="currentPage" :totalPages="totalPages" :fetchData="fetchIssues" />
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
import RequestsFilterSidebar from '@/components/RequestsFilterSidebar.vue';
import { createInfoModal } from '@/services/modal';
import ConfirmModal from '@/components/ConfirmModal.vue';
import Loading from '@/components/Loading.vue';

const store = useStore();
const showModal = ref(false);
const currentIssueToRevoke = ref(null);
const confirmModalMessage = ref('Are you sure you want to revoke this issue? ');
const isLoading = ref(false);

const issues = ref([]);
const totalPages = ref(0);
const currentPage = ref(1);

const searchQuery = ref('');
const selectedBooks = computed(() => store.getters.selectedBooks);
const selectedUserEmail = computed(() => store.getters.selectedUserEmail);



const fetchIssues = async (page) => {
    isLoading.value = true;
    let modal = null;
    try {
        const queryParams = new URLSearchParams({
                query: searchQuery.value,
                books: selectedBooks.value.map(book => book.id),
                userEmail: selectedUserEmail.value,
            }).toString();

        const response = await axios.get(`issues/all?page=${page}&per_page=11&${queryParams}`);
        isLoading.value = false;

        issues.value = response.data.issues;
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


const revokeIssue = (issue) => {
    currentIssueToRevoke.value = issue.id;
    confirmModalMessage.value = `Are you sure you want to revoke the issue <ID: ${issue.id} >?`;
    showModal.value = true;
};


const onConfirmed = async () => {
    showModal.value = false;
    isLoading.value = true;
    let modal = null;

    try {
        await axios.delete(`issues/revoke/${currentIssueToRevoke.value}`);
        modal = createInfoModal("Success", "Book Issue revokeed successfully.");
    } catch (error) {
        console.error(error);

        if(error.response && error.response.data){
            modal = createInfoModal("Error", error.response.data.message);
        } else{
            modal = createInfoModal("Error", "An error occurred.");
        }
    }
    currentIssueToRevoke.value = null;
    isLoading.value = false;
    modal.show();

};

const onCancelled = () => {
    showModal.value = false;
    currentIssueToRevoke.value = null;
};



onMounted(async () => {
   await fetchIssues(currentPage.value);

   var confirmModal = document.getElementById('confirmModal');
    if (confirmModal) {
        confirmModal.addEventListener('hidden.bs.modal', function (event) {
            currentIssueToRevoke.value = null;
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