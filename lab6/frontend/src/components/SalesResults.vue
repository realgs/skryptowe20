<template>
  <div>
    <div class="sales-chart" v-if="results">
      <canvas ref="salesChart"></canvas>
    </div>

    <div class="sales-results" v-if="results">
      <b-table
        hover
        :items="results"
        head-variant="light"
        outlined
        :fields="fields"
      >
      </b-table>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js";

export default {
  name: "SalesResults",
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
          key: "original_total",
          label: "Sales in USD",
        },
        {
          key: "exchanged_total",
          label: "Sales in PLN",
        },
      ],
    };
  },
  watch: {
    results() {
      if (this.chart != null) this.chart.destroy();
      if (this.results && this.results.length > 1) this.renderSalesChart();
    },
  },
  methods: {
    async renderSalesChart() {
      const chartData = {
        labels: [],
        datasets: [
          {
            label: "USD",
            data: [],
            backgroundColor: "rgba(33, 113, 181, 0.6)",
          },
          {
            label: "PLN",
            data: [],
            backgroundColor: "rgb(203, 24, 29, 0.4)",
          },
        ],
      };

      for (let item of this.results) {
        chartData.labels.push(item.date);
        chartData.datasets[0].data.push(item.original_total);
        chartData.datasets[1].data.push(item.exchanged_total);
      }

      await this.$nextTick();
      const ctx = this.$refs.salesChart.getContext("2d");
      this.chart = new Chart(ctx, {
        type: "line",
        data: chartData,
        options: {
          title: {
            display: true,
            text: "Sales in the bike shop over time",
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
                  labelString: "Total sales revenue",
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
.sales-results {
  margin: 50px 25% 50px 25%;
}
.sales-chart {
  margin: 50px 15% 50px 15%;
}
</style>
