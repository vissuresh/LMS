<template>
    <div class="btn-group btn-warning" role="group">
        <template v-for="num in 5">
        <input type="radio" class="btn-check" :name="'rating' + num" :id="'rating' + num" :value="num" v-model="rating" @click="selectRating(num)">
        <label class="btn btn-outline-primary btn-sm " :for="'rating' + num">{{ num }}</label>
        </template>
        <button class="btn btn-outline-primary btn-sm btn-outline-danger " @click="selectRating(0)">Clear</button>
    </div>
</template>


<script setup>
import { ref, defineEmits } from 'vue';
const rating = ref(0);

const emits = defineEmits(['updateValue']);

const selectRating = (num) => {
    rating.value = num;
    emits('updateValue', num);
}

</script>