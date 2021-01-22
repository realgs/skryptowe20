import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'

import Home from "./components/Home.vue";
import Sale from "./components/Sale.vue";
import Sales from "./components/Sales.vue";
import Rate from "./components/Rate.vue";
import Rates from "./components/Rates.vue";
import Chartkick from 'vue-chartkick'
import Chart from 'chart.js'

Vue.use(Chartkick.use(Chart))
Vue.use(VueRouter)

const routes = [
    {path: '/', component: Home},
    {path: '/sale', component: Sale},
    {path: '/sales', component: Sales},
    {path: '/rate', component: Rate},
    {path: '/rates', component: Rates}
]

const router = new VueRouter({
    routes,
    mode: 'history'
})
Vue.config.productionTip = false

new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
