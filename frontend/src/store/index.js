import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: !!localStorage.getItem('isAuthenticated'),
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
  },
  mutations: {
    setAuthenticated(state, value) {
      state.isAuthenticated = value;
      localStorage.setItem('isAuthenticated', value);
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
