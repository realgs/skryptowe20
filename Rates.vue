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

      <button class="searchButton" v-on:click="searchApiRate" style="margin-left: 50px;">Search</button>
    </div>
    <div style="margin-top: 20px; min-height: 20px;">
      <label id="errorLabel" style="color: #cc2222"></label>
    </div>
    <table id="currencyTable" class="dataTable">
      <div>
        <tr>
          <td>Date</td>
          <td>Rates in PLN</td>
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
export default {
name: "Rates"
}
</script>

<style scoped>

</style>