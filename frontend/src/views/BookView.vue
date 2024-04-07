<template>
    <div class="container">
        <div class="row mb-5">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ book.name }}</h5>
                        <p class="card-text">{{ book.desc }}</p>
                        <button class="btn btn-primary" @click="handleRequestBook">Request Book</button>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <img :src="book.picture" class="card-img-top" alt="Book Picture">
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-12">
                <div class="row mb-3">
                    <div class="col-md-12">
                        <h5 class="card-title">Comments</h5>
                    </div>
                </div>
                <div v-for="comment in comments" :key="comment.id" class="row mb-3">
                    <div class="col-md-12">
                        <div class="card">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-center">
                                    <div>{{ comment.user }}</div>
                                    <div>{{ comment.comment }}</div>
                                    <div class="badge bg-primary">{{ comment.rating }}</div>
                                </div>
                            </div>
                        </div>
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
import { requestBook } from '@/services/requestBook.js';

const book = ref({});
const comments = ref([]);
const route = useRoute();
const id = ref(parseInt(route.params.id));

const  handleRequestBook = () => requestBook(id.value);




onMounted(async () => {
    try{
        const response = await axios.get(`books/${id.value}`);
        book.value = response.data;
    } catch(error) {
        console.error(error);
    }
    
    try {       
        const commentsResponse = await axios.get(`books/${id.value}/comments`);
        comments.value = commentsResponse.data;
    } catch (error) {
        console.error(error);
    }
});

</script>




<style>

</style>