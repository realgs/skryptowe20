<template>
  <div>
    <h1>Currency rate</h1>

    <div>
      <label for="currencyDate" style="margin: 20px;">Select date:</label>
      <input type="date" id="currencyDate" name="trip-start">

      <label style="margin-left: 60px; margin-right: 20px;">Select currency:</label>
      <select id="currency">
        <option>AUD</option>
        <option>BGN</option>
        <option>BYN</option>
        <option>CAD</option>
        <option>CHF</option>
        <option>CZK</option>
        <option>DKK</option>
        <option>EUR</option>
        <option>GBP</option>
        <option>HRK</option>
        <option>HUF</option>
        <option>JPY</option>
        <option>RON</option>
        <option>RUB</option>
        <option>SEK</option>
        <option>TRY</option>
        <option>UAH</option>
        <option>USD</option>
      </select>

      <button class="searchButton" v-on:click="loadRateFromApi()" style="margin-left: 50px;">Search</button>
    </div>
    <div style="margin-top: 20px; min-height: 20px;">
      <label id="errorLabel" style="color: #cc2222"></label>
    </div>
    <div class="tableWithFixHead" v-if="this.list !== undefined">
      <table id="currencyTable" class="dataTable">
        <thead>
        <tr style="background-color: #232323;">
          <th>Date</th>
          <th>Rates in PLN</th>
          <th>Was interpolated</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="item in list" v-bind:key="item.date">
          <td>{{ item.date }}</td>
          <td>{{ item.value }}</td>
          <td>{{ item.isInterpolated }}</td>
        </tr>
        </tbody>
      </table>
    </div>
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
  methods: {
    loadRateFromApi: function () {
      const selectedDate = document.getElementById("currencyDate").value;
      const selectElement = document.getElementById("currency");
      const selectedCurrency = selectElement.options[selectElement.selectedIndex].text;

      if (selectedDate !== "") {
        Vue.axios.get('http://127.0.0.1:5000/currency-rates/' + selectedCurrency + '/' + selectedDate)
            .then((resp) => {
              this.list = resp.data.rates
              this.changeErrorText('')
            })
            .catch(error => {
              this.list = undefined
              this.changeErrorText(error.response.data.message)
            })
      } else {
        this.changeErrorText('Please select a date')
      }
    },

    changeErrorText: function (text) {
      const errorText = document.getElementById("errorLabel");
      errorText.innerText = text
    }
  }
}
</script>