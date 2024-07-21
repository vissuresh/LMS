<template>
    <div class="container">
      <h1 class="mb-5">Librarian DashBoard</h1>
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
              <router-link to="/book-requests" class="btn btn-primary">Go to Book Requests</router-link>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card mb-4">
            <div class="card-body">
              <h5 class="card-title">Book Issues</h5>
              <p class="card-text">Manage and revoke book issuances.</p>
              <router-link to="/book-issues" class="btn btn-primary">Go to Book Issues</router-link>
            </div>
          </div>
        </div>
      </div>


    </div>
</template>