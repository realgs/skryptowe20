import Vue from 'vue';
import VueRouter from 'vue-router';
import Info from '@/components/Info.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Info',
    component: Info,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
