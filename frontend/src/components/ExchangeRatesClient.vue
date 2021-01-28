<template>
  <v-container
    class="spacing-playground pa-8"
    fluid
  >
    <v-row class="text-center">
      <v-col cols="12" lg="12">
        <h1 class="text-center">Exchange rates </h1>
      </v-col>
      <v-col
        cols="12"
        lg="6"
      >
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
          @change="resetChart"
          required
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
            @change="resetChart"
          ></v-date-picker>
        </v-menu>
        <p>Selected date: <strong>{{ selected.start_date }}</strong></p>

        <v-menu
          v-if="selected.range_of_days === 'From date to date'"
          ref="menu"
          :close-on-content-click="false"
          transition="scale-transition"
          offset-y
          max-width="290px"
          min-width="auto"
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
            min="2014-12-28"
            max="2016-12-28"
            show-current="2014-12-28"
            @change="resetChart"
          ></v-date-picker>
        </v-menu>
        <p v-if="selected.range_of_days === 'From date to date'">Selected end date:
          <strong>{{ selected.end_date }}</strong></p>
        <v-btn color="primary" v-on:click="sendRequest">Send request</v-btn>
        <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
        <br><br>
      </v-col>
      <v-col
        cols="12"
        lg="6"
      >
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-header>Response</v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-data-table
                :headers="headers"
                :items="this.response"
                :page.sync="page"
                hide-default-footer
                :items-per-page="itemsPerPage"
                class="elevation-1"
                @page-count="pageCount = $event"
              >
                <template v-slot:item.interpolated="{ item }">
                  <v-simple-checkbox
                    v-model="item.interpolated"
                    disabled
                  ></v-simple-checkbox>
                </template>
              </v-data-table>
              <div class="text-center pt-2">
                <v-pagination
                  v-model="page"
                  :length="pageCount"
                ></v-pagination>
                <v-text-field
                  :value="itemsPerPage"
                  label="Items per page"
                  type="number"
                  min="1"
                  max="100"
                  @input="itemsPerPage = parseInt($event, 10)"
                ></v-text-field>
              </div>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
    <br><br>
    <chart :chartdata="this.chart_data" :options="this.options"
           v-if="this.chart_data !== null">
    </chart>
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
      page: 1,
      pageCount: 0,
      itemsPerPage: 10,
      search: '',
      headers: [
        {
          text: 'Date',
          align: 'start',
          filterable: false,
          value: 'date',
        },
        {
          text: 'Currency',
          value: 'currency',
        },
        {
          text: 'Rate',
          value: 'rate',
        },
        {
          text: 'Interpolated',
          value: 'interpolated',
        },
      ],
      errors: [],
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
    checkAllRequired() {
      return this.selected.start_date !== '' && this.selected.range_of_days !== ''
        && this.selected.currency !== '' && ((this.selected.range_of_days === 'From date to date'
          && this.selected.end_date !== '') || this.selected.range_of_days === 'One day');
    },
    checkDateRange() {
      return this.selected.start_date <= this.selected.end_date;
    },
    checkDate(date) {
      return date >= Utils.MIN_DATE && date <= Utils.MAX_DATE;
    },
    checkRequiredData() {
      let errorMessages = [];
      errorMessages = [];
      if (this.selected.start_date === '') errorMessages.push('Please select start date.');
      if (this.selected.range_of_days === '') errorMessages.push('Please select range of days.');
      if (this.selected.currency === '') errorMessages.push('Please select currency.');
      if (this.selected.range_of_days === 'From date to date') {
        if (this.selected.end_date === '') errorMessages.push('Please select end date.');
      }
      if (this.checkAllRequired()) {
        errorMessages = [];
        if (!this.checkDate(this.selected.start_date)) {
          errorMessages.push('Start date is out of range.');
        }
        if (this.selected.range_of_days === 'From date to date') {
          if (!this.checkDate(this.selected.end_date)) {
            errorMessages.push('End date is out of range.');
          }
          if (!this.checkDateRange()) {
            errorMessages.push('Start date cant be after end date.');
          }
        }
      }
      if (errorMessages.length > 0) {
        this.errors = errorMessages;
      }
    },
    sendRequest() {
      this.checkRequiredData();
      if (this.errors.length === 0) {
        switch (this.selected.range_of_days) {
          case 'One day':
            this.resetChart();
            this.rateOneDay();
            break;
          case 'From date to date':
            this.resetChart();
            this.rateFromDateToDate();
            break;
          default:
            break;
        }
      }
    },
    resetChart() {
      this.errors = [];
      this.chart_data = null;
    },
    async rateOneDay() {
      this.hasResult = true;
      const path = `${Utils.SALES_EXCHANGE_RATES_URL}/${Utils.RATES_PATH}/${this.selected.currency}/${this.selected.start_date}`;
      await axios.get(path)
        .then((result) => {
          this.response = result.data.rates.map((el) => ({
            currency: el.currency,
            date: el.date,
            rate: el.rate,
            interpolated: el.interpolated,
          }));
          this.prepareRatesChartData();
        })
        .catch((error) => {
          console.log(error);
          console.error(error);
        });
    },
    async rateFromDateToDate() {
      this.hasResult = true;
      const path = `${Utils.SALES_EXCHANGE_RATES_URL}/${Utils.RATES_PATH}/${this.selected.currency}/${this.selected.start_date}/${this.selected.end_date}`;
      await axios.get(path)
        .then((result) => {
          this.response = result.data.rates.map((el) => ({
            currency: el.currency,
            date: el.date,
            rate: el.rate,
            interpolated: el.interpolated,
          }));
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
        dates.push(el.date);
        rates.push(el.rate);
      });
      this.chart_data = {
        labels: dates,
        datasets: [{
          label: this.selected.currency,
          borderColor: '#004D40',
          pointBackgroundColor: '#EF6C00',
          data: rates,
          fill: false,
        },
        ],
      };
      this.options.scales.yAxes[0].scaleLabel.labelString = 'Exchange rate';
      this.options.scales.xAxes[0].scaleLabel.labelString = 'Date';
    },
  },
};
</script>
