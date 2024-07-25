import { createStore } from 'vuex'

export default createStore({
  state: {
    authenticated: JSON.parse(localStorage.getItem('authenticated')) || false,
    librarian: JSON.parse(localStorage.getItem('librarian')) || false,

    selectedSections: [],
    selectedAuthors: [],
    selectedRating: 0,
    selectedBooks: [],
    selectedUserEmail: '',

    
  },
  mutations: {
    setAuthenticated(state, value) {
        state.authenticated = value;
        localStorage.setItem('authenticated', JSON.stringify(value));
    },

    setLibrarian(state, value) {
        state.librarian = value
        localStorage.setItem('librarian', JSON.stringify(value));
    },




    updateSelectedSections(state, sections) {
      state.selectedSections = sections;
    },
    updateSelectedAuthors(state, authors) {
      state.selectedAuthors = authors;
    },
    updateSelectedRating(state, rating) {
      state.selectedRating = rating;
    },
    updateSelectedBooks(state, books) {
      state.selectedBooks = books;
    },
    updateSelectedUserEmail(state, email) {
      state.selectedUserEmail = email;
    },

  },

  actions: {
    authenticated({ commit }, value) {
      commit('setAuthenticated', value);
    },

    librarian({ commit }, value) {
      commit('setLibrarian', value);
    },

    
    setFilters({ commit }, { sections, authors, rating }) {
      commit('updateSelectedSections', sections);
      commit('updateSelectedAuthors', authors);
      commit('updateSelectedRating', rating);
    },

    setBookRequestFilters({ commit }, { userEmail, books }) {
      commit('updateSelectedBooks', books);
      commit('updateSelectedUserEmail', userEmail);
    },

  },

  getters: {
    isAuthenticated(state) {
      return state.authenticated;
    },
    isLibrarian(state) {
      return state.librarian;
    },

    selectedSections(state) {
      return state.selectedSections;
    },

    selectedAuthors(state) {
      return state.selectedAuthors;
    },

    selectedRating(state) {
      return state.selectedRating;
    },

    selectedBooks(state) {
      return state.selectedBooks;
    },

    selectedUserEmail(state) {
      return state.selectedUserEmail;
    },
  }

})