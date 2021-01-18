<template>
  <div>
    <h1>Currency rate</h1>
    <table>
      <div>
        <label for="currencyDate" style="margin: 20px;">Select date:</label>

        <input type="date" id="currencyDate" name="trip-start">
        <label style="margin-left: 60px;">Select currency:</label>

        <select id="currency">
          <option value="aud">AUD</option>
          <option value="aud">BYN</option>
          <option value="aud">BGN</option>
          <option value="aud">HRK</option>
          <option value="aud">DKK</option>
          <option value="aud">JPY</option>
          <option value="aud">CAD</option>
          <option value="aud">CZK</option>
          <option value="aud">RUB</option>
          <option value="aud">RON</option>
          <option value="aud">USD</option>
          <option value="aud">CHF</option>
          <option value="aud">SEK</option>
          <option value="aud">TRY</option>
          <option value="aud">EUR</option>
          <option value="aud">UAH</option>
          <option value="aud">HUF</option>
          <option value="aud">GBP</option>
        </select>

        <button v-on:click="searchApiRate" style="margin-left: 30px;">Search</button>
      </div>
      <div style="margin-top: 40px; margin-left: 20px;">
        <tr>
          <td>Date</td>
          <td>Rate</td>
          <td>Is interpolated</td>
        </tr>
        <tr v-for="item in list" v-bind:key="item.date">
          <td>{{ item.date }}</td>
          <td>{{ item.value }}</td>
          <td>{{ item.isInterpolated }}</td>
        </tr>
      </div>
    </table>
  </div>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)
export default {
  name: "Rate",
  data() {
    return {
      list: undefined
    }
  },
  mounted() {
    document.getElementById("currencyDate").value
  },
  methods: {
    searchApiRate: function () {
      var selected_date = document.getElementById("currencyDate").value
      var selectElement = document.getElementById("currency")
      var selected_currency = selectElement.options[selectElement.selectedIndex].text
      console.warn(selected_currency)
      if (selected_date !== "") {
        console.warn(selected_date)
        Vue.axios.get('http://127.0.0.1:5000/currency-rates/' + selected_currency + '/' + selected_date)
            .then((resp) => {
              this.list = resp.data.rates
              console.warn(resp.data.rates)
            })
        if (this.list === undefined) {
          this.list = null
        }
      }
    }
  }
}
</script>

<style scoped>

</style>