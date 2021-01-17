<template>
	<v-app>
		<v-app-bar app color="white">
			<v-tabs v-model="currentTab" fixed-tabs>
				<v-tab>
					Exchange Rates
				</v-tab>
				<v-tab>
					Sales
				</v-tab>
				<v-tab>
					Readme
				</v-tab>
			</v-tabs>
		</v-app-bar>

		<v-main>
			<v-tabs-items v-model="currentTab">
				<v-tab-item> <exchange-rates /> </v-tab-item>
				<v-tab-item> <sales /> </v-tab-item>
				<v-tab-item> <readme /> </v-tab-item>
			</v-tabs-items>
		</v-main>
	</v-app>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import Readme from "@/views/Readme.vue";
import ExchangeRates from "@/views/ExchangeRates.vue";
import Sales from "@/views/Sales.vue";

@Component({
	components: {
		Readme,
		ExchangeRates,
		Sales
	}
})
export default class App extends Vue {
	currentTab = null;
}
</script>

<style>
.table-header {
	background-color: #1976d2 !important;
	color: white !important;
}
</style>
