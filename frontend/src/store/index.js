import { createStore, createLogger } from 'vuex'



const defaultState = () => {
  return {
  }

}


export default createStore({
  plugins: [createLogger()],


  state: {
  },

  getters: {
  },

  mutations: {
    RESET_STATE(state) {
      Object.assign(state, defaultState());
    },
  },

  actions: {
    resetState({ commit }) {
      commit('RESET_STATE');
    },

  },

  modules: {
  }
});

