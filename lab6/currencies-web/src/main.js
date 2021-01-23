import Vue from 'vue'
import store from './store/store'
import VCalendar from 'v-calendar'
import App from './App'
import router from './router/index'
import VueSimpleMarkdown from 'vue-simple-markdown'
import 'vue-simple-markdown/dist/vue-simple-markdown.css'

Vue.use(VueSimpleMarkdown)
Vue.use(VCalendar)
new Vue({
    render: h => h(App),
    router,
    store,
}).$mount('#app')






