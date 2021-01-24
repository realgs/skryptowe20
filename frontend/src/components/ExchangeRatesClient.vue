<template>
  <v-container
    class="spacing-playground pa-8"
    fluid
  >
    <v-row class="text-center">
      <v-col
        cols="12"
        lg="6"
      >
        <h1 class="text-center">Exchange rates
        </h1>
        <b-alert class="mb-5" variant="danger" :show="errors != null"
        ><ul>
          <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
        </ul></b-alert
        >
        <br><br>
        <v-select
          :items="range_of_days"
          label="Select a range of days"
          v-model="selected.range_of_days"
          required
        ></v-select>

        <v-select
          :items="currencies"
          label="Select currency"
          v-model="selected.currency"
          required
        ></v-select>

        <v-menu
          ref="menu"
          :close-on-content-click="false"
          transition="scale-transition"
          offset-y
          max-width="290px"
          min-width="auto"
          @change="resetChart"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              label="Select date"
              persistent-hint
              prepend-icon="mdi-calendar"
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="selected.start_date"
            no-title
            min="2014-12-28"
            max="2016-12-28"
            show-current="2014-12-28"
            @input="rate_one_day"
          ></v-date-picker>
        </v-menu>
        <p>Selected date: <strong>{{ selected.start_date }}</strong></p>

        <v-menu
          v-if="selected.range_of_days === 'from date to date'"
          ref="menu"
          :close-on-content-click="false"
          transition="scale-transition"
          offset-y
          max-width="290px"
          min-width="auto"
          @change="resetChart"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              label="Select end date"
              persistent-hint
              prepend-icon="mdi-calendar"
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="selected.end_date"
            no-title
            @input="rate_from_date_to_date"
          ></v-date-picker>
        </v-menu>
        <p v-if="selected.range_of_days === 'from date to date'">Selected end date:
          <strong>{{ selected.end_date }}</strong></p>
        <b-form @submit="onSubmit">
          <b-button type="submit" variant="primary">Send request</b-button>
        </b-form>
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
          <b-table
            hover
            :items="response"
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

      </v-col>
    </v-row>
    <v-row align="center" class="ma-4">
      <v-expansion-panels>
        <v-expansion-panel>
          <v-expansion-panel-header>Response</v-expansion-panel-header>
          <v-expansion-panel-content><pre>{{response}}</pre></v-expansion-panel-content>
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
import Utils from './Utils.vue';

export default {
  name: 'ExchangeRatesClient',
  data() {
    return {
      errors: null,
      showError: false,
      response: null,
      hasResult: false,
      currencies: Utils.CURRENCIES,
      range_of_days: ['One day', 'From date to date'],
      date: new Date().toISOString()
        .substr(0, 10),
      available_dates: {
        min_date: Utils.MIN_DATE,
        max_date: Utils.MAX_DATE,
      },
      selected: {
        start_date: '',
        end_date: '',
        currency: '',
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
    async onSubmit(event) {
      event.preventDefault();
      const errors = [];
      if (this.selected.start_date == null) errors.push('Starting date is empty');
      if (this.selected.end_date == null) errors.push('Ending date is empty');
      if (errors.length > 0) {
        this.errors = errors;
      }
    },

    resetChart() {
      this.chartdata = null;
    },
    async rate_one_day() {
      this.hasResult = true;
      const path = `${Utils.SALES_EXCHANGE_RATES_URL}/${Utils.RATES_PATH}/${this.selected.currency}/${this.selected.start_date}`;
      await axios.get(path)
        .then((result) => {
          this.response = result.data.rates;
          this.prepareRatesChartData();
        })
        .catch((error) => {
          console.log(error);
          console.error(error);
        });
    },

    async rate_from_date_to_date() {
      this.hasResult = true;
      const path = `${Utils.SALES_EXCHANGE_RATES_URL}/${Utils.RATES_PATH}/${this.selected.currency}/${this.selected.start_date}/${this.selected.end_date}`;
      await axios.get(path)
        .then((result) => {
          this.response = result.data.rates;
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
      let rates = [];
      rates = [];
      this.response.forEach((el) => {
        console.log(el);
        console.log(el.date);
        console.log(el.rate);
        dates.push(el.date);
        rates.push(el.rate);
      });
      this.chart_data = {
        labels: dates,
        datasets: [{
          label: 'Exchange rates chart',
          borderColor: '#004D40',
          pointBackgroundColor: '#EF6C00',
          data: rates,
          fill: false,
        },
        ],
      };
      console.log(this.chart_data);
      this.options.scales.yAxes[0].scaleLabel.labelString = 'Sales value';
      this.options.scales.xAxes[0].scaleLabel.labelString = 'Date';
    },
  },
};
</script>
