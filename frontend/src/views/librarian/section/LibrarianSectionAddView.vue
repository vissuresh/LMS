<template>
    <Loading :isLoading="isLoading" />
    <div class="container ">
        <div class="card">
            <div class="card-title mb-5 text-center">
                <h2>Add Section</h2>
            </div>
            <div class="row g-0">
                <div class="col-md-8">
                    <div class="card-body">
                        <form @submit.prevent="saveSection" class="needs-validation" novalidate>
                            <div class="mb-3 input-group">
                                <label for="name" class="col-sm-2 col-form-label">Name:</label>
                                <input type="text" id="name" v-model="newSection.name" class="form-control" required />
                                
                            </div>
                                
                            <div class="mb-3 input-group">
                                <label for="description" class="col-sm-2 col-form-label">Description:</label>
                                <textarea id="description" v-model="newSection.desc" class="form-control" required></textarea>
                                
                            </div>

                            <button type="submit" class="btn btn-primary">Save</button>
                        </form>
                    </div>

                </div>
            </div>
            
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { createInfoModal } from '@/services/modal';
import Loading from '@/components/Loading.vue';

const isLoading = ref(false);
const operationSuccess = ref(false);
const newSection = ref({
    name: '',
    desc: '',
});
1
const saveSection = async () => {
    Object.keys(newSection.value).forEach(key => {
        if (!newSection.value[key]) {
            const modal = createInfoModal('Error',`Incomplete information. Please fill all fields`);
            modal.show();
            return;
        }
    });

    let modal = null;
    isLoading.value = true;

    let formData = new FormData();
    formData.append('data', JSON.stringify(newSection.value));

    try{
        const response = await axios.post(`/sections`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        operationSuccess.value = true;
        modal = createInfoModal('Created','Section saved successfully');
    } catch (error) {
        if(error.response && error.response.data){
            modal = createInfoModal('Error',error.response.data.message);
        } else{
            modal = createInfoModal('Error','An error occurred.');
        }    
    }
    isLoading.value = false;
    modal.show();
};

onMounted(() => {
    var myModalEl = document.getElementById('infoModal');
    if (myModalEl) {
        myModalEl.addEventListener('hidden.bs.modal', function (event) {
            if (operationSuccess.value == true){
                window.location.reload();
            }
        });
    }
});
</script>

<style scoped>
.card {
    max-width: 90%;
    margin-right: auto;
  margin-left: auto;
}
</style>