<template>
	<v-container fluid
		><v-row class="pt-6" style="height: 640px;" justify="center">
			<v-col cols="4" class="text-center">
				<span class="pa-4">
					Select dates range to generate report from
				</span>
				<v-date-picker
					:width="380"
					range
					:min="minDate"
					:max="maxDate"
					:picker-date.sync="initialPickerDate"
					v-model="selectedDates"
					:selected-items-text="datesText"
					@change="onDatesChange"
					elevation="3"
				>
					<v-spacer />
					<v-btn
						color="primary"
						elevation="3"
						:disabled="selectedDates.length != 2"
						@click="getSalesData"
					>
						Show report
					</v-btn></v-date-picker
				>
			</v-col>
			<v-col cols="8">
				<v-row>
					<v-col cols="6">
						<v-data-table
							class="pt-6"
							:items="salesData"
							:headers="tableHeaders"
							fixed-header
						>
							<template v-slot:item.date="{ item }">
								<span> {{ item.date.substring(0, 10) }} </span>
							</template>
						</v-data-table>
					</v-col>
					<v-col cols="6" v-if="salesData.length">
						<custom-chart
							:chart-data="chartData"
							:options="chartOptions"
						/>
					</v-col>
				</v-row>
			</v-col> </v-row
	></v-container>
</template>

<script lang="ts">
import { Component, Vue, Inject } from "vue-property-decorator";
import ApiClient from "@/api/ApiClient";
import { SaleData } from "@/api/TypeDefs";
import moment from "moment";
import { DataTableHeader } from "vuetify";
import { ChartOptions, ChartData } from "chart.js";
import CustomChart from "@/components/CustomChart.vue";

@Component({ components: { CustomChart } })
export default class Sales extends Vue {
	@Inject() apiClient!: ApiClient;

	initialPickerDate = "2003-10";
	minDate = "2003-10-26";
	maxDate = "2004-08-24";

	selectedDates: string[] = [];
	salesData: SaleData[] = [];

	chartData: ChartData = {};
	chartOptions: ChartOptions = {};

	mounted() {
		this.onResize();
		window.addEventListener("resize", this.onResize, { passive: true });
	}

	beforeDestroy() {
		window.removeEventListener("resize", this.onResize);
	}

	get tableHeaders(): DataTableHeader[] {
		return [
			{
				text: "Date",
				value: "date",
				class: "table-header"
			},
			{
				text: "USD",
				value: "USD",
				class: "table-header"
			},
			{
				text: "PLN",
				value: "PLN",
				class: "table-header"
			}
		];
	}

	get datesText() {
		if (this.selectedDates.length === 0) return "";

		let from = this.selectedDates[0];
		let to = this.selectedDates[1];

		// Handle case when `from` was selected after `to`
		if (from > to) {
			from = [to, (to = from)][0];
		}
		return (
			moment(from).format("ddd, MMM D YYYY") +
			" - " +
			moment(to).format("ddd, MMM D YYYY")
		);
	}

	async getSalesData() {
		let from = this.selectedDates[0];
		let to = this.selectedDates[1];

		// Handle case when `from` was selected after `to`
		if (from > to) {
			from = [to, (to = from)][0];
		}

		this.salesData = await this.apiClient.getSalesInRange(from, to);
		this.updateChart(this.salesData);
	}

	updateChart(response: SaleData[]) {
		this.chartData = {
			labels: response.map(x => x.date.substring(0, 10)),
			datasets: [
				{
					label: "Total sales in USD",
					data: response.map(x => Number(x.USD)),
					backgroundColor: "transparent",
					borderColor: "rgba(1, 116, 188, 0.50)",
					pointBackgroundColor: "rgba(171, 71, 188, 1)"
				},
				{
					label: "Total sales in PLN",
					data: response.map(x => Number(x.PLN)),
					backgroundColor: "transparent",
					borderColor: "rgba(1, 188, 116, 0.50)",
					pointBackgroundColor: "green"
				}
			]
		};
	}

	// Cannot select the same date as `from` and `to`
	onDatesChange(e: any) {
		if (typeof e[1] != "undefined" && e[0] == e[1]) {
			this.selectedDates = this.selectedDates.slice(0, 1);
		}
	}

	// Dynamically spread fixed header
	onResize() {
		const wrapper = document.getElementsByClassName(
			"v-data-table__wrapper"
		)[1] as HTMLDivElement;

		if (wrapper) {
			wrapper.style.maxHeight =
				window.innerWidth > 1888 ? "70vh" : "62vh";
			wrapper.style.height = "100%";
		}
	}
}
</script>

<style scoped></style>
