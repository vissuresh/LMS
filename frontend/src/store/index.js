import { createStore } from 'vuex'

export default createStore({
  state: {
    authenticated: JSON.parse(localStorage.getItem('authenticated')) || false,
    librarian: JSON.parse(localStorage.getItem('librarian')) || false
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

  },

  actions: {
    authenticated({ commit }, value) {
      commit('setAuthenticated', value);
    },

    librarian({ commit }, value) {
      commit('setLibrarian', value);
    },

  },

  getters: {
    isAuthenticated(state) {
      return state.authenticated;
    },
    isLibrarian(state) {
      return state.librarian;
    },
  }

})