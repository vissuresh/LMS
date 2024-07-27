import { createStore } from 'vuex'

export default createStore({
  state: {
    authenticated: JSON.parse(localStorage.getItem('authenticated')) || false,
    librarian: JSON.parse(localStorage.getItem('librarian')) || false,

    selectedSectionIds: [],
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




    updateSelectedSectionIds(state, section_ids) {
      state.selectedSectionIds = section_ids;
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

    
    setFilters({ commit }, { section_ids, authors, rating }) {
      commit('updateSelectedSectionIds', section_ids);
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

    selectedSectionIds(state) {
      return state.selectedSectionIds;
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