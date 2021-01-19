<template>
  <div>
    <h1>Currency rate</h1>

    <div>
      <label for="currencyDate" style="margin: 20px;">Select date:</label>
      <input type="date" id="currencyDate" name="trip-start">

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

      <button class="searchButton" v-on:click="searchApiRate" style="margin-left: 50px;">Search</button>
    </div>
    <div style="margin-top: 20px; min-height: 20px;">
      <label id="errorLabel" style="color: #cc2222"></label>
    </div>
    <table id="currencyTable" class="dataTable">
      <div>
        <tr>
          <td>Date</td>
          <td>Rate in PLN</td>
          <td>Was interpolated</td>
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
  methods: {
    searchApiRate: function () {
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

<style scoped>
</style>