import Vue from 'vue';
import VueRouter from 'vue-router';
import DailyRates from '../components/DailyRate.vue';
import Home from '../components/Home.vue';
import Rates from '../components/Rates.vue';
import DailySale from '../components/DailySale.vue';
import Sales from '../components/Sales.vue';

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/daily_rates',
      name: 'DailyRate',
      component: DailyRates,
    },
    {
      path: '/daily_sales',
      name: 'DailySale',
      component: DailySale,
    },
    {
      path: '/rates',
      name: 'Rates',
      component: Rates,
    },
    {
      path: '/sales',
      name: 'Sales',
      component: Sales,
    },
  ],
});

export default router;
