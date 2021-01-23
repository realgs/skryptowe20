<template>
  <div>
    <h1>Currency rates</h1>

    <div>
      <label for="currencyDateFrom" style="margin: 20px;">Select start date:</label>
      <input type="date" id="currencyDateFrom" name="trip-start">

      <label for="currencyDateTo" style="margin: 20px;">Select end date:</label>
      <input type="date" id="currencyDateTo" name="trip-start">

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

      <button class="searchButton" v-on:click="searchForRates" style="margin-left: 50px;">Search</button>
    </div>
    <div style="margin-top: 20px; min-height: 20px;">
      <label id="errorLabel" style="color: #cc2222"></label>
    </div>
    <div class="tableWithFixHead" v-if="this.list !== undefined">
      <table id="currencyTable" class="dataTable">
        <thead>
        <tr style="position: sticky; top: 0; background-color: #232323;">
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
    <div style="margin-top: 50px;">
    <column-chart id="ratesChart" v-if="this.list !== undefined" :data="ratesData"
                  style="margin: auto; width: 73%; background-color: #232323"></column-chart>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import axios from 'axios'
import VueAxios from 'vue-axios'
import Chartkick from 'vue-chartkick'

Vue.use(VueAxios, axios)
export default {
  name: "Rates",
  data() {
    return {
      list: undefined,
      ratesData: {},
      apiRates: []
    }
  },
  methods: {
    searchForRates: function () {
      const selectedDateFrom = document.getElementById("currencyDateFrom").value;
      const selectedDateTo = document.getElementById("currencyDateTo").value;
      const selectElement = document.getElementById("currency");
      const selectedCurrency = selectElement.options[selectElement.selectedIndex].text;

      if (selectedDateFrom !== "" && selectedDateTo !== "") {
        this.loadRatesFromApi(selectedCurrency, selectedDateFrom, selectedDateTo)
            .then(() => {
              this.updateRatesData(selectedCurrency)
            })
            .catch(() => {
              this.updateRatesData(selectedCurrency)
            })
      } else {
        this.changeErrorText('Please select a date')
      }
    },

    loadRatesFromApi: function (selectedCurrency, selectedDateFrom, selectedDateTo) {
      return new Promise((resolve, reject) => {
        Vue.axios.get('http://127.0.0.1:5000/currency-rates/' +
            selectedCurrency + '/' + selectedDateFrom + '/' + selectedDateTo)
            .then((resp) => {
              this.list = resp.data.rates
              this.changeErrorText('')
              resolve()
            })
            .catch(error => {
              this.list = undefined
              this.changeErrorText(error.response.data.message)
              reject()
            })
      })
    },

    updateRatesData: function (selectedCurrency) {
      this.apiRates = []
      if (this.list !== undefined) {
        this.list.forEach(apiRate => {
          const {
            date,
            value
          } = apiRate

          this.apiRates.push([date, value])
        })
      }

      this.ratesData = [
        {
          name: selectedCurrency + '-PLN rates',
          data: this.apiRates,
          color: '#ffffff',
          textStyle: '#ffffff'
        }
      ]

      const chart = Chartkick.charts["ratesChart"]
      chart.updateData(this.ratesData)
    },

    changeErrorText: function (text) {
      if(text.includes("per")){
        text = "Too many requests, the limit is " + text
      }
      const errorText = document.getElementById("errorLabel");
      errorText.innerText = text
    }
  }
}
</script>