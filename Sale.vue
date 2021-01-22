<template>
  <div>
    <h1>Sale from one day</h1>

    <div>
      <label for="saleDate" style="margin: 20px;">Select date:</label>
      <input type="date" id="saleDate" name="trip-start">

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

      <button class="searchButton" v-on:click="loadSaleFromApi()" style="margin-left: 50px;">Search</button>
    </div>
    <div style="margin-top: 20px; min-height: 20px;">
      <label id="errorLabel" style="color: #cc2222"></label>
    </div>
    <div class="tableWithFixHead" v-if="this.list !== undefined">
      <table id="currencyTable" class="dataTable">
        <thead>
        <tr style="background-color: #232323;">
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
  </div>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)
export default {
  name: "Sale",
  data() {
    return {
      list: undefined,
      chosenCurrency: "",
      originalCurrency: ""
    }
  },
  methods: {
    loadSaleFromApi: function () {
      const selectedDate = document.getElementById("saleDate").value;
      const selectElement = document.getElementById("currency");
      const selectedCurrency = selectElement.options[selectElement.selectedIndex].text;

      if (selectedDate !== "") {
        Vue.axios.get('http://127.0.0.1:5000/sales/' + selectedCurrency + '/' + selectedDate)
            .then((resp) => {
              this.list = resp.data.sales
              this.chosenCurrency = resp.data.chosenCurrency
              this.originalCurrency = resp.data.originalCurrency
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