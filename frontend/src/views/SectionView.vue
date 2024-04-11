<template>
    <div class="container">
        <div class="row mb-5">
            <div class="co">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ section.name }}</h5>
                        <p class="card-text">{{ section.desc }}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-12">
                <div class="row mb-3">
                    <div class="col-md-12">
                        <h5 class="card-title">Popular Books</h5>
                    </div>
                </div>
                <div v-for="book in sectionBooks" :key="book.id" class="row mb-3">
                    <div class="col-md-12">
                        <div class="card">
                            <div class="card-body">
                                <div class="col">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div>{{ book.name }}</div>
                                        <div>{{ book.desc }}</div>
                                    </div>
                                </div>

                                <div class="col-4">
                                    <img :src="book.picture" class="card-img-top" :alt="book.desc">
                                    <button class="btn btn-warning">
                                        <router-link :to="`/books/${book.id}`">View More</router-link>
                                    </button>
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

const section = ref({});
const sectionBooks = ref([]);

const route = useRoute();
const id = ref(parseInt(route.params.id));




onMounted(async () => {
    try{
        const response = await axios.get(`sections/${id.value}`);
        section.value = response.data;
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