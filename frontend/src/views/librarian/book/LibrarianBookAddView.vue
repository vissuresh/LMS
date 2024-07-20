<template>
    <Loading :isLoading="isLoading" />
    <div class="container ">
        <div class="card">
            <div class="card-title mb-5 text-center">
                <h2>Add Book</h2>
            </div>
            <div class="row g-0">
                <div class="col-md-8">
                    <div class="card-body">
                        <form @submit.prevent="saveBook" class="needs-validation" novalidate>
                            <div class="mb-3 input-group">
                                <label for="name" class="col-sm-2 col-form-label">Name:</label>
                                <input type="text" id="name" v-model="newBook.name" class="form-control" required />
                                
                            </div>

                            <div class="mb-3 input-group">
                                <label for="author" class="col-sm-2 col-form-label">Author:</label>
                                <input type="text" id="author" v-model="newBook.author" class="form-control" required />
                            </div>
                                
                            <div class="mb-3 input-group">
                                <label for="description" class="col-sm-2 col-form-label">Description:</label>
                                <textarea id="description" v-model="newBook.desc" class="form-control" required></textarea>
                                
                            </div>

                            <div class="mb-3 input-group">
                                <label for="section" class="col-sm-2 col-form-label">Section:</label>
                                <select id="section" v-model="newBook.section_id" class="form-select" placeholder="" required>
                                    <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
                                </select>
                                
                            </div>

                            <div class="mb-3 input-group">
                                <label for="copies" class="col-sm-2 col-form-label">No. of Copies:</label>
                                <input type="number" id="copies" v-model="newBook.copies" class="form-control" required min="0" />
                            </div>

                            <div class="mb-3 input-group">
                                <label for="picture" class="col-sm-2 col-form-label">Picture:</label>
                                <input type="file" id="picture" @change="onPictureChange" accept="image/*" class="form-control" required/>
                                
                            </div>

                            <div class="mb-3 input-group">
                                <label for="book_file" class="col-sm-2 col-form-label">Book File:</label>
                                <input type="file" id="book_file" @change="onFileChange" class="form-control" required/>
                                
                            </div>

                            <button type="submit" class="btn btn-primary">Save</button>
                        </form>
                    </div>

                </div>
                <div class="col-md-4 d-flex justify-content-center align-items-center">
                    <img v-if="newBook.picture" :src="'data:image/jpeg;base64,' + newBook.picture" class="img-fluid rounded-start" alt="Book Picture">
                    <span v-else>|| No Picture selected ||</span>
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
const newBook = ref({
    name: '',
    author: '',
    desc: '',
    section_id: '',
    copies: null,
    picture: '',
    book_file: null
});
const sections = ref([]);


const fetchSections = async () => {
    try {
        const response = await axios.get('/sections/all');
        sections.value = response.data.sections;
    } catch (error) {
        console.error(error);
    }
};

const onPictureChange = (e) => {
    if (!e.target.files.length) {
        newBook.value.picture = '';
        return;
    }
    
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onloadend = () => {
        newBook.value.picture = reader.result.split(',')[1];
    };
    reader.readAsDataURL(file);
};

const onFileChange = (e) => {
    if (!e.target.files.length) {
        newBook.value.book_file = null;
        return;
    }
    newBook.value.book_file = e.target.files[0];
};


const saveBook = async () => {
    Object.keys(newBook.value).forEach(key => {
        if (!newBook.value[key]) {
            const modal = createInfoModal('Error',`Incomplete information. Please fill all fields`);
            modal.show();
            return;
        }
    });

    let modal = null;
    isLoading.value = true;

    let formData = new FormData();
    if (newBook.value.book_file) {
        formData.append('file', newBook.value.book_file);
    }
    newBook.book_file = null;
    formData.append('data', JSON.stringify(newBook.value));

    try{
        const response = await axios.post(`/books`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        operationSuccess.value = true;
        modal = createInfoModal('Created','Book saved successfully');
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
    fetchSections();

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

img {
    max-width: 70%;
    height: auto;
}
</style>