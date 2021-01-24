<template>
  <v-container
    class="spacing-playground pa-8"
    fluid
  >
  <v-row class="text-left">
    <v-col class="mb-4" cols="12">
      <h1 class="text-center">Exchange rates and sales API</h1>
    </v-col>
    <v-col class="mb-4" cols="12">
      <h2>
        Info
      </h2>
      <p></p>
      <p> This API provides exchange rates of three currencies (USD, EUR, GBP)
        and data on total sales in two currencies - original (USD)
        and converted at the exchange rate of the National Bank of Poland (PLN).</p>
      <p>Exchange rate data and sales data are from 2014-12-28 to 2016-12-28.</p>
      <p>
        Date format used is <b>YYYY-MM-DD</b>, e.g. 2015-10-13. </p>
      <p>
        Exchange rate data - property <i>interpolated</i> is set to <b>true</b> for days that had
        no value and took their value from the previous (or next, depending on the situation)
        day that had the exchange rate. <b>False</b> otherwise.
      </p>
    </v-col>
    <v-col class="mb-4" cols="12">
      <h2>
        Endpoints
      </h2>
      <p></p>
      <p><b>There are currently four endpoints you can use:</b></p>
      <ul>
        <li><h3>/exchange-rates/{currency}/{date}</h3></li>
        <p>Provides exchange rate of the selected currency on the selected date.
          <span class="brown--text"><b>For example:</b> /exchange-rates/GBP/2015-10-13</span></p>
        <v-btn
          href="http://sale-and-exchange-rate.herokuapp.com/exchange-rates/GBP/2015-10-13"
          depressed
          color="accent"
          rounded
        >
          Check out this example
        </v-btn>
        <p></p>
        <li><h3>/exchange-rates/{currency}/{start_date}/{end_date}</h3></li>
        <p>Provides exchange rates of the selected currency on the selected time period.
          <span class="brown--text"><b>For example:</b>
            /exchange-rates/EUR/2015-10-13/2015-10-18</span>
        </p>
        <v-btn
          href="http://sale-and-exchange-rate.herokuapp.com/exchange-rates/EUR/2015-10-13/2015-10-18"
          depressed
          color="accent"
          rounded
        >
          Check out this example
        </v-btn>
        <p></p>
        <li><h3>/sales/{date}</h3></li>
        <p>Provides sales data for the selected date.
          <span class="brown--text"><b>For example:</b> /sales/2016-10-13</span></p>
        <v-btn
          href="http://sale-and-exchange-rate.herokuapp.com/sales/2016-10-13"
          depressed
          color="accent"
          rounded
        >
          Check out this example
        </v-btn>
        <p></p>
        <li><h3>/sales/{start_date}/{end_date}</h3></li>
        <p>Provides sales data for the selected time period.
          <span class="brown--text"><b>For example:</b> /sales/2016-10-13/2016-10-19</span></p>
        <v-btn
          href="http://sale-and-exchange-rate.herokuapp.com/sales/2016-10-13/2016-10-19"
          depressed
          color="accent"
          rounded
        >
          Check out this example
        </v-btn>
      </ul>
    </v-col>
    <v-col class="mb-4" cols="12">
      <h2>
        Limits
      </h2>
      <p></p>
      <p>Requests limit is set to <b>500 per day</b> and <b>30 per hour</b>, both per user.
        After exceeding the limit, the client will receive the <b>HTTP 429 Too Many Requests</b>
        response status code.</p>
    </v-col>
    <v-col class="mb-4" cols="12">
      <h2>
        Cache
      </h2>
      <p></p>
      <p>Project provides an application caching mechanism.
        Application stores exchange rates and sales data to reference later.
        Cache timeout is set to <b>24 hours</b>.</p>
    </v-col>
    <v-col class="mb-4" cols="12">
      <h2>
        Looking for more information?
      </h2>
      <p></p>
      <p>For all documentation, installation instructions and code - visit my Github:</p>
      <v-btn
        href="https://github.com/joannasroka/skryptowe20/tree/L5"
        depressed
        color="primary"
        large
      >
        Github
      </v-btn>
    </v-col>
  </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'Info',
};
</script>

<style scoped>
p {
  font-size: 18px;
}
</style>
