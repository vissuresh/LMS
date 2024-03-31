import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: localStorage.getItem('isAuthenticated') === null ? false : JSON.parse(localStorage.getItem('isAuthenticated')),
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
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
  },
  actions: {
    updateAuthenticated({ commit }, value) {
      commit('setAuthenticated', value);
    },
  },
  modules: {
  }
})
