import Vuex from "vuex"
import Vue from 'vue'
import main from './main';
import dataPanel from './dataPanel'

Vue.use(Vuex)

const store = new Vuex.Store({
    strict: true,
    modules: {
        main,
        dataPanel
    }
})
export default store;

