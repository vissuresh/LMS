<template>
    <ExportModal />
    <div class="container">
      <div class="row mb-5">
        <div class="col-10">
          <h1>Librarian DashBoard</h1>
        </div>
        <div class="col">
          <button class="btn btn-success" @click="exportCSV">Export CSV</button>
        </div>
      </div>
      
      <div class="row">
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-body">
              <h5 class="card-title">Books</h5>
              <p class="card-text">Add, Update or Delete Books.</p>
              <router-link to="/librarian/books" class="btn btn-primary">Go to Books</router-link>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-body">
              <h5 class="card-title">Sections</h5>
              <p class="card-text">Add, Update or Delete Sections.</p>
              <router-link :to="{ name: 'LibrarianSections' }" class="btn btn-primary">Go to Sections</router-link>
            </div>
          </div>
        </div>
      </div>


      <div class="row">
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-body">
              <h5 class="card-title">Book Requests</h5>
              <p class="card-text">Approve or reject book requests.</p>
              <router-link :to="{ name: 'LibrarianBookRequests' }" class="btn btn-primary">Go to Book Requests</router-link>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-body">
              <h5 class="card-title">Book Issues</h5>
              <p class="card-text">Manage and revoke book issuances.</p>
              <router-link :to="{ name: 'LibrarianBookIssues' }" class="btn btn-primary">Go to Book Issues</router-link>
            </div>
          </div>
        </div>
      </div>


    </div>
</template>


<script setup>
import { onMounted, } from 'vue';
import { createInfoModal, createCSVModal } from '@/services/modal';
import ExportModal from '@/components/ExportModal.vue';
import axios from 'axios';


const exportCSV = async () => {
  let modal = null;

    try {
      const response = await axios.get('/tasks/export-csv');
      modal = createInfoModal('Export CSV', "Task has been created. You will be notified");
    } 
    catch (error) {
        if(error.response && error.response.data){
          modal = createInfoModal('Request', error.response.data.message);
        } else {
          modal = createInfoModal('Request', 'An error occurred.');
        } 
    }
    modal.show();
};


onMounted(async () => {
  const eventSource = new EventSource('http://127.0.0.1:5000/stream', {withCredentials:true});

  eventSource.addEventListener('task_status', (event) => {
    console.log('Connection to server opened.');
    const data = JSON.parse(event.data);
    
    if(data.status === 'SUCCESS') {
        const status = 'CSV generation complete!';
        const downloadUrl = `data:text/csv;charset=utf-8,${encodeURIComponent(data.csv_data)}`;

        createCSVModal(status, downloadUrl).show();
    }
  });

  // eventSource.onmessage = (event) => {
  //   const data = JSON.parse(event.data);
  //   console.log("Task status: ", data);
  //   if (data.type === 'task_status' && data.status === 'SUCCESS') {
  //       const status = 'CSV generation complete!';
  //       const downloadUrl = `data:text/csv;charset=utf-8,${encodeURIComponent(data.csv_data)}`;

  //       createInfoModal(status, `Click here to download: ${downloadUrl}`).show()
  //   }
  // }

  eventSource.onerror = function(event) {
    console.error('EventSource failed:', event);
  };




  var myModalEl = document.getElementById('infoModal');
    if (myModalEl) {
        myModalEl.addEventListener('hidden.bs.modal', function (event) {
              window.location.reload();
        });
    }


  var csvModalEl = document.getElementById('csvModal');
    if (csvModalEl) {
        csvModalEl.addEventListener('hidden.bs.modal', function (event) {
              window.location.reload();
        });
    }
});
</script>