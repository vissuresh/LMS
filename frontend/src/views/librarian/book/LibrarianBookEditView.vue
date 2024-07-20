<template>
    <Loading :isLoading="isLoading" />
    <div class="container ">
        <div class="card">
            <div class="card-title mb-5 text-center">
                <h2>Edit Book</h2>
            </div>
            <div class="row g-0">
                <div class="col-md-8">
                    <div class="card-body">
                        <form @submit.prevent="saveBook" class="needs-validation" novalidate>
                            <div class="mb-3 input-group">
                                <label for="name" class="col-sm-2 col-form-label">Name:</label>
                                <input type="text" id="name" v-model="newBook.name" :disabled="!editableFields.name" class="form-control" required />
                                <div class="input-group-text">
                                    <input type="checkbox" v-model="editableFields.name" class="form-check-input" @change="toggleEditable('name')" />
                                </div>
                                
                            </div>

                            <div class="mb-3 input-group">
                                <label for="author" class="col-sm-2 col-form-label">Author:</label>
                                <input type="text" id="author" v-model="newBook.author" :disabled="!editableFields.author" class="form-control" required />
                                <div class="input-group-text"><input type="checkbox" v-model="editableFields.author" class="form-check-input" @change="toggleEditable('author')" /></div>
                            </div>

                            <div class="mb-3 input-group">
                                <label for="description" class="col-sm-2 col-form-label">Description:</label>
                                <textarea id="description" v-model="newBook.desc" :disabled="!editableFields.desc" class="form-control" required></textarea>
                                <div class="input-group-text">
                                    <input type="checkbox" v-model="editableFields.desc" class="form-check-input" @change="toggleEditable('desc')" />
                                </div>
                            </div>

                            <div class="mb-3 input-group">
                                <label for="section" class="col-sm-2 col-form-label">Section:</label>
                                <select id="section" v-model="newBook.section_id" :disabled="!editableFields.section_id" class="form-select" placeholder="">
                                    <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
                                </select>
                                <div class="input-group-text">
                                    <input type="checkbox" v-model="editableFields.section_id" class="form-check-input" @change="toggleEditable('section_id')" />
                                </div>
                            </div>

                            <div class="mb-3 input-group">
                                <label for="copies" class="col-sm-2 col-form-label">No. of Copies:</label>
                                <input type="number" id="copies" v-model="newBook.copies" :disabled="!editableFields.copies" class="form-control" required />
                                <span class="input-group-text" id="issued">Issued: {{book.issued}}</span>
                                <div class="input-group-text">
                                    <input type="checkbox" v-model="editableFields.copies" class="form-check-input" @change="toggleEditable('copies')" />
                                </div>
                            </div>

                            <div class="mb-3 input-group">
                                <label for="picture" class="col-sm-2 col-form-label">Picture:</label>
                                <input type="file" id="picture" :disabled="!editableFields.picture" @change="onPictureChange" accept="image/*" class="form-control" />
                                <div class="input-group-text">
                                    <input type="checkbox" v-model="editableFields.picture" class="form-check-input" @change="toggleEditable('picture')" />
                                </div>
                            </div>

                            <div class="mb-3 input-group">
                                <label for="book_file" class="col-sm-2 col-form-label">Book File:</label>
                                <input type="file" id="book_file" :disabled="!editableFields.book_file" @change="onFileChange" class="form-control" />
                                <div class="input-group-text">
                                    <input type="checkbox" v-model="editableFields.book_file" class="form-check-input" @change="toggleEditable('book_file')" />
                                </div>
                            </div>

                            <button type="submit" class="btn btn-primary">Save</button>
                        </form>
                    </div>

                </div>
                <div class="col-md-4 d-flex justify-content-center align-items-center">
                    <img :src="'data:image/jpeg;base64,' + newBook.picture" class="img-fluid rounded-start" alt="Book Picture">
                </div>
            </div>
            
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { createInfoModal } from '@/services/modal';
import Loading from '@/components/Loading.vue';

const isLoading = ref(false);
const operationSuccess = ref(false);
const newBook = ref({});
const book = ref({});
const editableFields = ref({
    name: false,
    author: false,
    desc: false,
    section_id: false,
    copies: false,
    book_file: false,
});
const sections = ref([]);
const route = useRoute();
const router = useRouter();
const bookId = route.params.bookId;


const fetchBook = async () => {
    try{
        const response = await axios.get(`/books/${bookId}`);
        book.value = {...response.data, book_file: null, section_id: response.data.section.id};     
        newBook.value = {...response.data, book_file: null, section_id: response.data.section.id};
        
    } catch (error) {
        console.error(error);
    }
    
};

const fetchSections = async () => {
    try {
        const response = await axios.get('/sections/all');
        sections.value = response.data.sections;
    } catch (error) {
        console.error(error);
    }
};

const onPictureChange = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onloadend = () => {
        newBook.value.picture = reader.result.split(',')[1];
    };
    reader.readAsDataURL(file);
};

const onFileChange = (e) => {
    newBook.value.book_file = e.target.files[0];
};


const saveBook = async () => {
    isLoading.value = true;
    let modal = null;

    let formData = new FormData();
    if (newBook.value.book_file) {
        formData.append('file', newBook.value.book_file);
    }
    const data = {};
    Object.keys(editableFields.value).forEach(key => {
        if (editableFields.value[key]) {
            data[key] = newBook.value[key];
        }
    });
    formData.append('data', JSON.stringify(data));

    try{
        const response = await axios.patch(`/books/${bookId}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        operationSuccess.value = true;
        modal = createInfoModal('Edit','Book saved successfully');

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
        if(field === 'book_file') {
            document.getElementById('book_file').value = '';
        }

        else if (field === 'picture') {
            document.getElementById('picture').value = '';
        }

        newBook.value[field] = book.value[field];
    }
};

onMounted(() => {
    fetchBook();
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