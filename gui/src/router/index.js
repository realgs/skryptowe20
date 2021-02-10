import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import ExchangeRates from '../views/ExchangeRates.vue'
import Transactions from '../views/Transactions.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/exchangerates',
    name: 'Exchange rates',
    component: ExchangeRates
  },
  {
    path: '/transactions',
    name: 'Transactions',
    component: Transactions
  }
]

const router = new VueRouter({
  routes
})

export default router
