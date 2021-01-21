<template>
  <div>
    <div class="rates-chart" v-if="results">
      <canvas ref="ratesChart"></canvas>
    </div>

    <div class="rates-results" v-if="results">
      <b-table
        hover
        :items="results"
        head-variant="light"
        outlined
        :fields="fields"
      >
        <template #cell(interpolated)="data">
          <b-form-checkbox
            v-model="data.item.interpolated"
            disabled
          ></b-form-checkbox>
        </template>
      </b-table>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js";

export default {
  name: "RatesResults",
  props: {
    results: Array,
  },
  data() {
    return {
      chart: null,
      fields: [
        {
          key: "date",
          label: "Date",
        },
        {
          key: "interpolated",
          label: "Is interpolated?",
        },
        {
          key: "rate",
          label: "USD rate",
        },
      ],
    };
  },
  watch: {
    results() {
      if (this.chart != null) this.chart.destroy();
      if (this.results && this.results.length > 1) this.renderRatesChart();
    },
  },
  methods: {
    async renderRatesChart() {
      const chartData = {
        labels: [],
        datasets: [
          {
            label: "USD rate [PLN]",
            data: [],
            backgroundColor: "rgba(33, 113, 181, 0.4)",
          },
        ],
      };

      for (let item of this.results) {
        chartData.labels.push(item.date);
        chartData.datasets[0].data.push(item.rate);
      }

      await this.$nextTick();
      const ctx = this.$refs.ratesChart.getContext("2d");
      this.chart = new Chart(ctx, {
        type: "line",
        data: chartData,
        options: {
          title: {
            display: true,
            text: "USD exchange rate in PLN over time",
          },
          legend: {
            display: false,
          },
          scales: {
            xAxes: [
              {
                scaleLabel: {
                  display: true,
                  labelString: "Date",
                },
              },
            ],
            yAxes: [
              {
                scaleLabel: {
                  display: true,
                  labelString: "PLN value",
                },
              },
            ],
          },
        },
      });
    },
  },
};
</script>

<style scoped>
.rates-results {
  margin: 50px 25% 50px 25%;
}
.rates-chart {
  margin: 50px 15% 50px 15%;
}
</style>
