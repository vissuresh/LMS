<template>
    <div class="dropdown mb-5">
        <input type="text" class="form-control mb-2" :placeholder="`Search ${title}`" v-model="searchQuery">

        <div class="dropdown-menu w-100" :class="{ show: searchQuery.length }">
          <a v-for="option in filteredOptions" :key="option.id" @click="selectOption(option)" class="dropdown-item" href="#">
            {{ option.name }}
          </a>
        </div>

        <div class="tags">
            <span v-for="selected in selectedOptions" :key="selected.id" class="badge badge-pill rounded-pill text-bg-light">{{ selected.name }}
                <button type="button" class="btn-close" @click="removeOption(selected)" aria-label="Close"></button>
            </span>
        </div>

    </div>
</template>


<script setup>
import { ref, computed, defineProps, defineEmits } from 'vue';

const emits = defineEmits(['updateValue']);
const props = defineProps({
    options: {
    type: Array,
    default: () => []
     },
    title: {
        type: String,
    },
});

const searchQuery = ref('');
const selectedOptions = ref([]);

const filteredOptions = computed(() => {

  return props.options.filter(option =>
    option.name.toLowerCase().includes(searchQuery.value.toLowerCase().trim()) &&
    !selectedOptions.value.includes(option)
  );
});

const selectOption = (option) => {
  if (!selectedOptions.value.includes(option)) {
    selectedOptions.value.push(option);
    emits('updateValue', selectedOptions);
  }
  searchQuery.value = '';
};

const removeOption = (option) => {
  const index = selectedOptions.value.indexOf(option);
  if (index > -1) {
    selectedOptions.value.splice(index, 1);
  }
  emits('updateValue', selectedOptions);
};
</script>

<style scoped>



.dropdown-menu {
    max-height: 200px;
    overflow-y: auto;
}

.tags {
  gap: 0.2rem; 
  display: flex;
  flex-wrap: wrap;
  padding: 0;
}


.btn-close {
  
}



</style>