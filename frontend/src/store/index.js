import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: localStorage.getItem('isAuthenticated') === null ? false : JSON.parse(localStorage.getItem('isAuthenticated')),

    isLibrarian: localStorage.getItem('isLibrarian') === null ? false : JSON.parse(localStorage.getItem('isLibrarian')),

    userBooks: [],
    userRequests: [],

    current_page_books: [],
    next_page_books: [],
  },

  getters: {
    isAuthenticated: state => state.isAuthenticated,
    isLibrarian: state => state.isLibrarian,

    userBooks: state => state.userBooks,
    userRequests: state => state.userRequests,
  },

  mutations: {
    setAuthenticated(state, value) {
      state.isAuthenticated = value;
      if (value) {
        localStorage.setItem('isAuthenticated', value);
      } else {
        localStorage.removeItem('isAuthenticated');
      }
    },
    setLibrarian(state, value) {
      state.isLibrarian = value;
      if (value) {
        localStorage.setItem('isLibrarian', value);
      } else {
        localStorage.removeItem('isLibrarian');
      }
    },

    setUserBooks(state, value) {
      state.userBooks = value;
    },
    addUserBook(state, value) {
      state.userBooks.push(value);
    },
    removeUserBook(state, value) {
      state.userBooks = state.userBooks.filter(book => book.id !== value);
    },

    setUserRequests(state, value) {
      state.userRequests = value;
    },
    addUserRequest(state, value) {
      state.userRequests.push(value);
    },
    removeUserRequest(state, value) {
      state.userRequests = state.userRequests.filter(request => request.id !== value);
    },


  },

  actions: {
    updateAuthenticated({ commit }, value) {
      commit('setAuthenticated', value);
    },
    updateLibrarian({ commit }, value) {
      commit('setLibrarian', value);
    },

    updateUserBooks({ commit }, value) {
      commit('setUserBooks', value);
    },
    addUserBook({ commit }, value) {
      commit('addUserBook', value);
    },
    removeUserBook({ commit }, value) {
      commit('removeUserBook', value);
    },


    updateUserRequests({ commit }, value) {
      commit('setUserRequests', value);
    },
    addUserRequest({ commit }, value) {
      commit('addUserRequest', value);
    },
    removeUserRequest({ commit }, value) {
      commit('removeUserRequest', value);
    },


  },

  modules: {
  }
})
