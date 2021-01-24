<template>
  <v-container
    class="spacing-playground pa-8"
    fluid
  >
    <v-row class="text-left">
      <v-col
        cols="12"
        lg="6"
      >
        <h1 class="text-center">Sales</h1>
        <br><br>
        <v-select
          :items="range_of_days"
          label="Choose range of days"
          v-model="selected.range_of_days"
          required
          @change="resetChart"
        ></v-select>

        <v-menu
          ref="menu"
          :close-on-content-click="false"
          transition="scale-transition"
          offset-y
          max-width="290px"
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              label="Date"
              persistent-hint
              prepend-icon="mdi-calendar"
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="selected.start_date"
            no-title
            @input="sale_one_day"
          ></v-date-picker>
        </v-menu>
        <p>Selected start date: <strong>{{ selected.start_date }}</strong></p>

        <v-menu
          v-if="selected.range_of_days === 'from date to date'"
          ref="menu"
          :close-on-content-click="false"
          transition="scale-transition"
          offset-y
          max-width="290px"
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              label="Date"
              persistent-hint
              prepend-icon="mdi-calendar"
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="selected.end_date"
            no-title
            @input="sale_from_date_to_date"
          ></v-date-picker>
        </v-menu>
        <p v-if="selected.range_of_days === 'from date to date'">Selected end date:
          <strong>{{ selected.end_date }}</strong></p>

        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">Date</th>
            <th scope="col">Rate</th>
            <th scope="col">Interpolated</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="rt in response" v-bind:key="rt.date">
            <td>{{ rt.currency }}</td>
            <td>{{ rt.date }}</td>
            <td>{{ rt.rate }}</td>
            <td>
              <span v-if="rt.interpolated">Yes</span>
              <span v-else>No</span>
            </td>
          </tr>
          </tbody>
        </table>
      </v-col>
    </v-row>
    <v-row align="center" class="ma-4">
      <v-expansion-panels>
        <v-expansion-panel>
          <v-expansion-panel-header>Response</v-expansion-panel-header>
          <v-expansion-panel-content>
            <pre>{{ response }}</pre>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-row>
    <chart :chartdata="this.chart_data" :options="this.options"
           v-if="this.chart_data !== null"></chart>
  </v-container>
</template>

<script>
import axios from 'axios';
import Chart from './Chart.vue';

export default {
  name: 'Client',
  data() {
    return {
      response: null,
      hasResult: false,
      range_of_days: ['one day', 'from date to date'],
      date: new Date().toISOString()
        .substr(0, 10),
      available_dates: {
        min_date: '2014-12-28',
        max_date: '2016-12-28',
      },
      selected: {
        start_date: '',
        end_date: '',
        range_of_days: '',
      },
      rates: {
        currency: [],
        date: [],
        interpolated: [],
        rate: 0,
      },
      chart_data: null,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: '',
            },
            ticks: {
              maxTicksLimit: 10,
              autoSkip: true,
            },
          }],
          xAxes: [{
            scaleLabel: {
              display: true,
              label: '',
            },
            ticks: {
              maxTicksLimit: 10,
              autoSkip: true,
            },
          }],
        },
      },
    };
  },
  components: {
    Chart,
  },
  watch: {
    response() {
      if (this.response && this.response.length >= 1) this.prepareRatesChartData();
    },
  },
  methods: {
    resetChart() {
      this.chartdata = null;
    },
    async sale_one_day() {
      this.hasResult = true;
      const path = `https://sale-and-exchange-rate.herokuapp.com/sales/${this.selected.start_date}`;
      console.log(path);
      await axios.get(path)
        .then((result) => {
          this.response = result.data.sales;
          this.prepareRatesChartData();
        })
        .catch((error) => {
          console.log(error);
          console.error(error);
        });
    },

    async sale_from_date_to_date() {
      this.hasResult = true;
      const path = `https://sale-and-exchange-rate.herokuapp.com/sales/${this.selected.start_date}/${this.selected.end_date}`;
      await axios.get(path)
        .then((result) => {
          this.response = result.data.sales;
          this.prepareRatesChartData();
        })
        .catch((error) => {
          console.log(error);
          console.error(error);
        });
    },
    prepareRatesChartData() {
      let dates = [];
      dates = [];
      let pln = [];
      pln = [];
      let usd = [];
      usd = [];
      this.response.forEach((el) => {
        dates.push(el.date);
        pln.push(el.pln);
        usd.push(el.usd);
      });
      this.chart_data = {
        labels: dates,
        datasets: [{
          label: 'Sales pln',
          borderColor: '#f87979',
          pointBackgroundColor: '#000000',
          data: pln,
          fill: false,
        },
        {
          label: 'Sales usd',
          borderColor: '#1649b3',
          pointBackgroundColor: '#000000',
          data: usd,
          fill: false,
        },
        ],
      };
      console.log(this.chart_data);
      this.options.scales.yAxes[0].scaleLabel.labelString = 'Sales value';
      this.options.scales.xAxes[0].scaleLabel.labelString = 'Date';
    },
    created() {
      this.sale_one_day();
    },
  },
};
</script>
