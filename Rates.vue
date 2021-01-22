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
        <option value="aud">AUD</option>
        <option value="aud">BGN</option>
        <option value="aud">BYN</option>
        <option value="aud">CAD</option>
        <option value="aud">CHF</option>
        <option value="aud">CZK</option>
        <option value="aud">DKK</option>
        <option value="aud">EUR</option>
        <option value="aud">GBP</option>
        <option value="aud">HRK</option>
        <option value="aud">HUF</option>
        <option value="aud">JPY</option>
        <option value="aud">RON</option>
        <option value="aud">RUB</option>
        <option value="aud">SEK</option>
        <option value="aud">TRY</option>
        <option value="aud">UAH</option>
        <option value="aud">USD</option>
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
    <column-chart id="ratesChart" v-if="this.list !== undefined" :data="ratesData"
                  style="margin-top: 35px;"></column-chart>
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
      apiRates: [],
      rn: {
        "2021-01-05": 1.5,
        "2021-01-06": 2.5,
      }
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
          color: '#ffffff'
        }
      ]

      const chart = Chartkick.charts["ratesChart"]
      chart.updateData(this.ratesData)
    },

    changeErrorText: function (text) {
      const errorText = document.getElementById("errorLabel");
      errorText.innerText = text
    }
  }
}
</script>

<style scoped>
</style>