import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import ApiClient from "@/api/ApiClient";

Vue.config.productionTip = false;

new Vue({
	vuetify,
	render: h => h(App),
	provide: {
		apiClient: new ApiClient("http://127.0.0.1:5000/")
	}
}).$mount("#app");
