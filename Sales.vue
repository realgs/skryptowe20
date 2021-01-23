<template>
  <div>
    <h1>Sales in currency</h1>

    <div>
      <label for="salesDateFrom" style="margin: 20px;">Select start date:</label>
      <input type="date" id="salesDateFrom" name="trip-start">

      <label for="salesDateTo" style="margin: 20px;">Select end date:</label>
      <input type="date" id="salesDateTo" name="trip-start">

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
        <option>PLN</option>
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
          <th>Sale in {{ this.originalCurrency }}</th>
          <th v-if="chosenCurrency !== originalCurrency">Sale in {{ this.chosenCurrency }}</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="item in list" v-bind:key="item.date">
          <td>{{ item.date }}</td>
          <td>{{ item.saleOriginalCurrency }}</td>
          <td v-if="chosenCurrency !== originalCurrency">{{ item.saleCurrency }}</td>
        </tr>
        </tbody>
      </table>
    </div>
    <div style="margin-top: 50px;">
      <line-chart id="salesChart" v-if="this.list !== undefined" :data="salesData"
                  style="margin: auto; width: 73%; background-color: #232323"></line-chart>
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
  name: "Sales",
  data() {
    return {
      list: undefined,
      chosenCurrency: "",
      originalCurrency: "",
      salesData: {},
      apiOriginalCurrencySales: [],
      apiChosenCurrencySales: [],
    }
  },
  methods: {
    searchForRates: function () {
      const selectedDateFrom = document.getElementById("salesDateFrom").value;
      const selectedDateTo = document.getElementById("salesDateTo").value;
      const selectElement = document.getElementById("currency");
      const selectedCurrency = selectElement.options[selectElement.selectedIndex].text;

      if (selectedDateFrom !== "" && selectedDateTo !== "") {
        this.loadRatesFromApi(selectedCurrency, selectedDateFrom, selectedDateTo)
            .then(() => {
              this.updateSalesData(selectedCurrency)
            })
            .catch(() => {
              this.updateSalesData(selectedCurrency)
            })
      } else {
        this.changeErrorText('Please select a date')
      }
    },

    loadRatesFromApi: function (selectedCurrency, selectedDateFrom, selectedDateTo) {
      return new Promise((resolve, reject) => {
        Vue.axios.get('http://127.0.0.1:5000/sales/' +
            selectedCurrency + '/' + selectedDateFrom + '/' + selectedDateTo)
            .then((resp) => {
              this.list = resp.data.sales
              this.originalCurrency = resp.data.originalCurrency
              this.chosenCurrency = resp.data.chosenCurrency
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

    updateSalesData: function () {
      this.apiOriginalCurrencySales = []
      this.apiChosenCurrencySales = []
      if (this.list !== undefined) {
        this.list.forEach(apiSale => {
          if (this.originalCurrency !== this.chosenCurrency) {
            const {
              date,
              saleOriginalCurrency,
              saleCurrency,
            } = apiSale
            this.apiOriginalCurrencySales.push([date, saleOriginalCurrency])
            this.apiChosenCurrencySales.push([date, saleCurrency])
          } else {
            const {
              date,
              saleOriginalCurrency
            } = apiSale
            this.apiOriginalCurrencySales.push([date, saleOriginalCurrency])
          }
        })
      }

      if (this.originalCurrency !== this.chosenCurrency) {
        this.salesData = [
          {
            name: 'Sales in ' + this.originalCurrency,
            data: this.apiOriginalCurrencySales,
            color: '#ffffff'
          },
          {
            name: 'Sales in ' + this.chosenCurrency,
            data: this.apiChosenCurrencySales,
            color: '#e72f2f'
          }
        ]
      } else {
        this.salesData = [
          {
            name: 'Sales in ' + this.originalCurrency,
            data: this.apiOriginalCurrencySales,
            color: '#ffffff'
          }
        ]
      }

      const chart = Chartkick.charts["salesChart"]
      chart.updateData(this.salesData)
    },

    changeErrorText: function (text) {
      if(text.includes("per")){
        text = "Too many requests, the limit is " + text
      }
      const errorText = document.getElementById("errorLabel");
      errorText.innerText = text
    }
  },
}
</script>