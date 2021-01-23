<template>
  <div style="margin-top: 50px;">
    <h1> Welcome on the website that contains information on exchange rates and historical sales data</h1>
    <div style="display: flex;">
      <div class="apiDataContent">
        <h2>Sales</h2>
        <div style="margin-left: 40px; text-align: left;">
          <h3>Sale for one day is taken from:</h3>
          <p>http://localhost:5000/sales/currency/date</p>

          <h3 style="margin-top: 50px;">Sales for date period are taken from:</h3>
          <p>http://localhost:5000/sales/currency/date_from/date_to</p>

          <h3 style="margin-top: 50px; margin-bottom: 40px;">Sales are available for dates between 2011-05-31 and 2014-06-30</h3>
        </div>
      </div>
      <div class="apiDataContent">
        <h2>Rates</h2>
        <div style="margin-left: 40px; text-align: left;">
          <h3>Rate for one day is taken from:</h3>
          <p>http://localhost:5000/currency-rates/currency/date</p>

          <h3 style="margin-top: 50px;">Rates for date period are taken from:</h3>
          <p>http://localhost:5000/currency-rates/currency/date_from/date_to</p>

          <h3 style="margin-top: 50px; margin-bottom: 40px;">Rates are available from 2002-01-01</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
.apiDataContent {
  width: 45%;
  background-color: #3b3b3b;
  border-radius: 10px;
  margin-left: 3.33%;
}
</style>
