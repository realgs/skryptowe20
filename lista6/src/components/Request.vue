<template>
  <div>
    <button v-on:click="get_data">Send</button>

    <h3>Link: {{ request_url }}</h3>
    <h3>Status: {{ status }}</h3>
    <RatesTable v-if="this.is_rates === true" :response="response" :status="status" :key="request_url"/>
    <SalesTable v-else-if="this.is_sales === true" :response="response" :status="status" :key="request_url"/>

    <Chart v-if="this.is_rates === true && this.status === 200" :chart_data="rates_chart_data"/>
    <Chart v-else-if="this.is_sales === true && this.status === 200" :chart_data="sales_chart_data"/>

  </div>
</template>

<script>
import axios from 'axios';
import RatesTable from "@/components/tables/RatesTable";
import SalesTable from "@/components/tables/SalesTable";
import Chart from "@/components/charts/Chart";

export default {
  name: "Request",
  components: {
    SalesTable,
    RatesTable,
    Chart
  },
  data() {
    return {
      status: 0,
      response: [],
      rates_chart_data: {},
      sales_chart_data: {}
    }
  },
  props: {
    request_url: String,
    api_url: String,
    is_sales: Boolean,
    is_rates: Boolean
  },
  methods: {
    get_data() {
      axios.get(this.request_url)
          .then((response) => {
            this.response = response.data;
            this.status = 200;
            if (this.is_rates)
              this.set_rates_chart_data(response.data)
            if (this.is_sales)
              this.set_sales_chart_data(response.data)
          })
          .catch((error) => {
            this.status = error.response.status;
          })
          .finally(() => {

          });
    },
    set_rates_chart_data(resp) {
      let dates = [];
      let values = [];
      resp.forEach((item) => {
        dates.push(item['RateDate']);
        values.push(item['Exchange']);
      });
      this.options.scales.yAxes[0].scaleLabel.labelString = `USD/PLN`;
      this.rates_chart_data = {
        labels: dates,
        datasets: [{
          label: `USD rates`,
          data: values,
          fill: true
        }],
      };
    },
    set_sales_chart_data(resp) {
      let dates = [];
      let usd = [];
      let pln = [];
      resp.forEach((item) => {
        dates.push(item['OrderDate']);
        usd.push(item['UsdPrice']);
        pln.push(item['PlnPrice']);
      });
      this.options.scales.yAxes[0].scaleLabel.labelString = `USD/PLN`;
      this.sales_chart_data = {
        labels: dates,
        datasets: [{
          label: 'usd sales',
          data: usd,
          backgroundColor: '#f87979',
          fill: true
        }, {
          label: 'pln sales',
          data: pln,
          backgroundColor: '#f87979',
          fill: true
        }],
      };
    }
  }
}
</script>

<style scoped>

</style>
