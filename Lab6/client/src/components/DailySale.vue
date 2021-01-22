<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Sales at day</h1>
        <br><br>
        <div class="container">
          <div class="col-lg-5 col-md-4 col-sm-4 col-xs-4 ">
          <label for="example-datepicker" class="label">Date </label>
          <input id="example-datepicker"
                 type="date"
                 v-model="selected.start_date"
                 @input="getMessage"
                 :min="avaliable_dates.date_start"
                 :max="avaliable_dates.date_end"
                 class="mb-2 form-control"/>
          </div>
        </div>
        <div v-if="this.exists">
        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">Date</th>
            <th scope="col">PLN </th>
            <th scope="col">USD</th>
            <th scope="col">Rate</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(sale, index) in sales" :key="index">
            <td>{{ sale.sales_date }}</td>
            <td>{{ sale.PLN_sales }}</td>
            <td>{{ sale.USD_sales }}</td>
            <td>{{ sale.rate }}</td>
          </tr>
          </tbody>
        </table>
        </div>
        <div v-else>
        <div class="container">
             <h3>There is no data for selected date</h3>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'daily_sale',
  data() {
    return {
      avaliable_dates: {
        date_start: '2013-01-01',
        date_end: '2014-12-31',
      },
      selected: {
        start_date: '2013-01-01',
      },
      sales: {
        PLN_sales: 0,
        USD_sales: 0,
        rate: 0,
        sales_date: '',
      },
      message: '',
      showMessage: false,
      exists: false,
    };
  },
  methods: {
    getMessage() {
      const path = `http://127.0.0.1:5000/sales/${this.selected.start_date}`;
      axios.get(path)
        .then((res) => {
          if (res.data.length !== 0) {
            this.sales = res.data;
            this.exists = true;
          } else {
            this.exists = false;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};

</script>

<style scoped>

</style>
