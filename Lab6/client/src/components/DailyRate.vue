<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Rates at day</h1>
        <br><br>
        <div class="container">
          <div class="col-lg-5 col-md-4 col-sm-4 col-xs-4 ">
          <label for="example-datepicker" class="label align-center">Date </label>
          <input id="example-datepicker"
                 type="date"
                 v-model="selected.start_date"
                 @input="getMessage"
                 :min="avaliable_dates.date_start"
                 :max="avaliable_dates.date_end"
                 class="mb-2 form-control align-center"/>
          </div>
        </div>
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
          <tr v-for="(rt, index) in rates" :key="index">
            <td>{{ rt.rating_date }}</td>
            <td>{{ rt.rate }}</td>
            <td>
              <span v-if="rt.interpolated">Yes</span>
              <span v-else>No</span>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'daily_rate',
  data() {
    return {
      avaliable_dates: {
        date_start: '2013-01-01',
        date_end: '2014-12-31',
      },
      msg: '321',
      mesg: '123',
      selected: {
        start_date: '2013-01-01',
      },
      rates: {
        rating_date: [],
        rate: 0,
        interpolated: [],
      },
      message: '',
      showMessage: false,
    };
  },
  methods: {
    getMessage() {
      this.mesg = this.selected.start_date;
      const path = `http://127.0.0.1:5000/rates/usd/${this.selected.start_date}`;
      axios.get(path)
        .then((res) => {
          console.log('resdata');
          this.rates = res.data;
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
