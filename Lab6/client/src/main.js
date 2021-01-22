import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';
import VCalendar from 'v-calendar';
import Vue from 'vue';
import App from './App.vue';
import router from './router';

// Use v-calendar & v-date-picker components
Vue.use(VCalendar, { componentPrefix: 'vc' });

Vue.use(BootstrapVue);

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
