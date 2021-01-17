<script lang="ts">
import { Line, mixins } from "vue-chartjs";
import { Component, Mixins, Prop } from "vue-property-decorator";
import { ChartOptions } from "chart.js";
const { reactiveProp } = mixins;

@Component
export default class extends Mixins(Line, reactiveProp) {
	@Prop() options: ChartOptions | undefined;

	mounted() {
		this.renderChart(this.chartData, this.options);
	}
}
</script>
