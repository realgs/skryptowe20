<template>
	<v-container fluid>
		<v-row class="pt-6" style="height: 640px;" justify="center">
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
						@click="getExchangeRates"
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
							:items="exchangeRates"
							:headers="tableHeaders"
							fixed-header
						>
							<template v-slot:item.date="{ item }">
								<span> {{ item.date.substring(0, 10) }} </span>
							</template>
							<template v-slot:item.currency="{ item }">
								<span>
									{{ item.currency }}
								</span>
								<v-tooltip right v-if="item.interpolated">
									<template v-slot:activator="{ on }">
										<v-icon v-on="on" color="red">
											help
										</v-icon>
									</template>
									<span>
										Interpolated from previous date
									</span>
								</v-tooltip>
							</template>
						</v-data-table>
					</v-col>
					<v-col cols="6" v-if="exchangeRates.length">
						<custom-chart
							:chart-data="chartData"
							:options="chartOptions"
						/>
					</v-col>
				</v-row>
			</v-col>
		</v-row>
	</v-container>
</template>

<script lang="ts">
import { Component, Vue, Inject } from "vue-property-decorator";
import moment from "moment";
import ApiClient from "@/api/ApiClient";
import CustomChart from "@/components/CustomChart.vue";
import { ChartData, ChartOptions } from "chart.js";
import { ExchangeRate } from "@/api/TypeDefs";
import { DataTableHeader } from "vuetify";

@Component({
	components: {
		CustomChart
	}
})
export default class ExchangeRates extends Vue {
	@Inject() apiClient!: ApiClient;

	labels: string[] = [];

	initialPickerDate = "2003-10";
	minDate = "2003-10-26";
	maxDate = "2004-08-24";

	selectedDates: string[] = [];
	interpolationMap: boolean[] = [];
	exchangeRates: ExchangeRate[] = [];

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
				text: "PLN for 1 USD",
				value: "currency",
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

	async getExchangeRates() {
		let from = this.selectedDates[0];
		let to = this.selectedDates[1];

		// Handle case when `from` was selected after `to`
		if (from > to) {
			from = [to, (to = from)][0];
		}

		this.exchangeRates = await this.apiClient.getExchangeRatesInRange(
			from,
			to
		);
		this.interpolationMap = this.exchangeRates.map(x => x.interpolated);

		this.updateChart(this.exchangeRates);
	}

	updateChart(response: ExchangeRate[]) {
		this.chartOptions = {
			tooltips: {
				callbacks: {
					label: item => {
						const isInterpolated = this.interpolationMap[
							item.index ?? -1
						];
						const tooltipText =
							item.value +
							(isInterpolated
								? " [Interpolated from previous date]"
								: "");
						return tooltipText;
					}
				}
			}
		};

		this.chartData = {
			labels: response.map(x => x.date.substring(0, 10)),
			datasets: [
				{
					label: "PLN for 1 USD",
					data: response.map(x => Number(x.currency)),
					backgroundColor: "transparent",
					borderColor: "rgba(1, 116, 188, 0.50)",
					pointBackgroundColor: context => {
						const isInterpolated = this.interpolationMap[
							context.dataIndex ?? -1
						];
						return isInterpolated ? "red" : "rgba(171, 71, 188, 1)";
					}
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
		)[0] as HTMLDivElement;

		if (wrapper) {
			wrapper.style.maxHeight =
				window.innerWidth > 1888 ? "70vh" : "62vh";
			wrapper.style.height = "100%";
		}
	}
}
</script>

<style scoped>
::v-deep .v-date-picker-title__date {
	align-self: center;
}

::v-deep .v-date-picker-title__date div {
	text-align: center;
	max-width: 290px;
}
</style>
