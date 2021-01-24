<template>
  <div>
    <h2>Fill in the form and click Submit in order to obtain the data</h2>

    <h3>Choose data you would like to obtain</h3>
    <label>
      <input  v-on:input="change_to_sales" type="radio" name="sales/exchange" id="sales_checkbox" value="sales"
      />sales data
    </label>

    <label>
      <input v-on:input="change_to_rates" type="radio" name="sales/exchange" id="rates_checkbox" value="rates"/>USD
      to PLN exchange
    </label>

    <h3>Choose if you would like to obtain the data for<br/> specified one day or for the chosen date range</h3>
    <label>
      <input v-on:input="change_date_range" type="radio" name="date/range" id="one_day_checkbox" value="one_day"
             checked/>specified day
    </label>

    <label>
      <input v-on:input="change_date_range" type="radio" name="date/range" id="dates_range_checkbox"
             value="date_range"/>date range
    </label>

    <div v-if="is_date_range === false">
      <h3>Choose date</h3>
      <label>
        <input v-model="date" type="date" id="date_select" min="2018-07-04" max="2020-05-06">
      </label>
    </div>

    <div v-if="is_date_range === true">
      <h3>Choose date range</h3>
      <p>Choose starting date</p>
      <label>
        <input v-model="start_date" type="date" id="start_date" min="2018-07-04" :max="end_date"/>
      </label>

      <p>Choose ending date</p>
      <label>
        <input v-model="end_date" type="date" id="end_date" :min="start_date" max="2020-05-06"/>
      </label>
    </div>

    <h3>Click submit</h3>
    <Request :request_url="request_url" :api_url="api_url" :is_rates="is_rates" :is_sales="is_sales"/>
    <p>Dollar exchange values were downloaded from http://api.nbp.pl/</p>

  </div>
</template>

<script>
import Request from "@/components/Request";

export default {
  name: "Form",
  components: {
    Request
  },
  data() {
    return {
      is_date_range: false,
      date: "",
      start_date: "2018-07-04",
      end_date: "2020-05-06",
      is_rates: false,
      is_sales: false,
      api_url: "http://127.0.0.1:5000/api/",
    }
  },
  computed: {
    request_url() {
      let url = this.api_url;

      if (this.is_sales) {
        url += "sales/"
      } else if (this.is_rates) {
        url += "rates/"
      } else {
        return;
      }

      if (this.is_date_range) {
        url += this.start_date + "/" + this.end_date + "/";
      } else {
        url += this.date + "/";
      }
      return url;
    }
  },
  methods: {
    change_date_range: function () {
      this.is_date_range = !this.is_date_range
    },
    change_to_sales() {
      this.is_sales = true;
      this.is_rates = false;
    },
    change_to_rates() {
      this.is_sales = false;
      this.is_rates = true;
    }
  }
}
</script>

<style scoped>

</style>
