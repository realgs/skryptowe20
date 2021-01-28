import Vue from 'vue';
import colors from 'vuetify/lib/util/colors';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false;

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
  theme: {
    themes: {
      light: {
        primary: colors.red.darken1,
        secondary: colors.red.lighten4,
        accent: colors.indigo.base,
      },
    },
  },
}).$mount('#app');
