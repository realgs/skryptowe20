<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Rates at date range</h1>
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
        <span v-if="this.is_chosen">
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
          </span>
        <span v-else>
          <h3>Please select dates</h3>
        </span>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Rates',
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
      rates: [{
        rating_date: [],
        rate: 0,
        interpolated: [],
      }],
      showMessage: false,
      is_chosen: '',
    };
  },
  methods: {
    getMessage() {
      if (this.selected.start_date !== '' && this.selected.end_date !== '') {
        this.is_chosen = true;
        const path = `http://127.0.0.1:5000/rates/usd/${this.selected.start_date}/${this.selected.end_date}`;
        axios.get(path)
          .then((res) => {
            console.log(res.data);
            this.rates = res.data;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      }
    },
  },
  created() {
    this.getMessage();
  },
};

</script>

<style scoped>

</style>
