<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Sales at date range</h1>
        <br><br>
        <div class="container" align="center">
          <div class="col-lg-8 col-md-8 col-sm-8 col-xs-8">
            <label for="start_date_input" class="label align-center">Start Date
              <input id="start_date_input"
                     type="date"
                     v-model="selected.start_date"
                     @input="getMessage"
                     :min="available_dates.date_start"
                     :max="selected.end_date"
                     class="mb-2 form-control align-center"/>
            </label>
            <label for="end_date_input" class="label align-center">End Date
              <input id="end_date_input"
                     type="date"
                     v-model="selected.end_date"
                     @input="getMessage"
                     :min="selected.start_date"
                     :max="available_dates.date_end"
                     class="mb-2 form-control align-center"/></label>

          </div>
        </div>
        <div v-if="this.is_chosen">
          <div v-if="this.data_exist">
            <div v-if="this.draw_chart" class="container">
              <line-chart :chart-data="datacollection"></line-chart>
            </div>
            <table class="table table-hover">
              <thead>
              <tr>
                <th scope="col">Date</th>
                <th scope="col">PLN</th>
                <th scope="col">USD</th>
                <th scope="col">Rate</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="(sale, index) in this.sales" :key="index">
                <td>{{ sale.sales_date }}</td>
                <td>{{ sale.PLN_sales }}</td>
                <td>{{ sale.USD_sales }}</td>
                <td>{{ sale.rate }}</td>
              </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            <h3>There is no data for selected range</h3>
          </div>
        </div>
        <div v-else>
          <h3>Please select dates</h3>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
import LineChart from './LineChart';

export default {
  name: 'Sales',
  components: {
    LineChart,
  },
  data() {
    return {
      available_dates: {
        date_start: '2013-01-01',
        date_end: '2014-12-31',
      },
      selected: {
        start_date: '2013-01-01',
        end_date: '',
      },
      sales: [{
        PLN_sales: 0,
        USD_sales: 0,
        rate: 0,
        sales_date: '',
      }],
      showMessage: false,
      is_chosen: '',
      datacollection: null,
      draw_chart: false,
      data_exist: false,
    };
  },
  mounted() {
    this.fillData();
  },
  methods: {
    getMessage() {
      if (this.selected.start_date !== '' && this.selected.end_date !== '') {
        this.is_chosen = true;
        const path = `http://127.0.0.1:5000/sales/${this.selected.start_date}/${this.selected.end_date}`;
        axios.get(path)
          .then((res) => {
            if (res.data.length > 0) {
              this.sales = res.data;
              this.data_exist = true;
              if (res.data.length > 1) {
                this.fillData();
                this.draw_chart = true;
              } else {
                this.draw_chart = false;
              }
            } else {
              this.data_exist = false;
              this.draw_chart = false;
            }
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      }
    },
    fillData() {
      this.datacollection = {
        labels: this.sales.map((S) => S.sales_date),
        datasets: [
          {
            label: 'PLN',
            borderColor: '#17a800',
            borderWidth: 3,
            lineTension: 0,
            fill: false,
            pointRadius: 0,
            data: this.sales.map((S) => S.PLN_sales),

          },
          {
            label: 'USD',
            borderColor: '#225fa8',
            borderWidth: 3,
            lineTension: 0,
            fill: false,
            pointRadius: 0,
            data: this.sales.map((S) => S.USD_sales),
          },
        ],
      };
    },
  },
  created() {
    this.getMessage();
  },
};

</script>

<style scoped>
</style>
