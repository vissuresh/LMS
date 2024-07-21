<template>
    <Loading :isLoading="isLoading" />
    <div class="container ">
        <div class="card">
            <div class="card-title mb-5 text-center">
                <h2>Edit Section</h2>
            </div>
            <div class="row g-0">
                <div class="col-md-8">
                    <div class="card-body">
                        <form @submit.prevent="saveSection" class="needs-validation" novalidate>
                            <div class="mb-3 input-group">
                                <label for="name" class="col-sm-2 col-form-label">Name:</label>
                                <input type="text" id="name" v-model="newSection.name" :disabled="!editableFields.name" class="form-control" required />
                                <div class="input-group-text">
                                    <input type="checkbox" v-model="editableFields.name" class="form-check-input" @change="toggleEditable('name')" />
                                </div>
                                
                            </div>

                            <div class="mb-3 input-group">
                                <label for="description" class="col-sm-2 col-form-label">Description:</label>
                                <textarea id="description" v-model="newSection.desc" :disabled="!editableFields.desc" class="form-control" required></textarea>
                                <div class="input-group-text">
                                    <input type="checkbox" v-model="editableFields.desc" class="form-check-input" @change="toggleEditable('desc')" />
                                </div>
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
import { useRoute } from 'vue-router';
import axios from 'axios';
import { createInfoModal } from '@/services/modal';
import Loading from '@/components/Loading.vue';

const isLoading = ref(false);
const operationSuccess = ref(false);
const newSection = ref({});
const section = ref({});
const editableFields = ref({
    name: false,
    desc: false,
});
const route = useRoute();
const sectionId = route.params.sectionId;


const fetchSection = async () => {
    try{
        const response = await axios.get(`/sections/${sectionId}`);
        section.value = {...response.data};     
        newSection.value = {...response.data};
        
    } catch (error) {
        console.error(error);
    }
    
};


const saveSection = async () => {
    isLoading.value = true;
    let modal = null;

    let formData = new FormData();
    const data = {};
    Object.keys(editableFields.value).forEach(key => {
        if (editableFields.value[key]) {
            data[key] = newSection.value[key];
        }
    });
    formData.append('data', JSON.stringify(data));

    try{
        const response = await axios.patch(`/sections/${sectionId}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        operationSuccess.value = true;
        modal = createInfoModal('Edit','Section saved successfully');

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

const toggleEditable = (field) => {
    editableFields[field] = !editableFields[field];
    if (!editableFields[field]) {
        newSection.value[field] = section.value[field];
    }
};

onMounted(() => {
    fetchSection();

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