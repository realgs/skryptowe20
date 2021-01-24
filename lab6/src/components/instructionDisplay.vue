<template>
  <v-container>
    <h1>Prototype of currency rates and sales API</h1>
    <p>
      API for obtaining different currency rates and sales data from Superstore
      database in USD and PLN.
    </p>
    <p>With the use of this API you can obtain following data:</p>
    <p>
      - Chosen currency to PLN exchange rate for specified date:
      <br />http://127.0.0.1:5000/api/v1/resources/rates/chosen_currency/search_date/
      <br />example usage <a
      href="http://127.0.0.1:5000/api/v1/resources/rates/eur/2010-09-09/">http://127.0.0.1:5000/api/v1/resources/rates/eur/2010-09-09/</a>
    </p>
    <p>
      - Chosen currency to PLN exchange rate for date range:
      <br />http://127.0.0.1:5000/api/v1/resources/rates/chosen_currency/start/end/
      <br />example usage
      <a
        href="http://127.0.0.1:5000/api/v1/resources/rates/eur/2018-10-10/2019-10-10/"
        >http://127.0.0.1:5000/api/v1/resources/rates/eur/2018-10-10/2019-10-10/</a
      >
      <br />
    </p>

    <p>
      - sales data for specified date:
      <br />http://127.0.0.1:5000/api/v1/resources/orders/dailyOrders/search_date/
      <br />example usage
      <a
        href="http://127.0.0.1:5000/api/v1/resources/orders/dailyOrders/2010-10-10/"
        >http://127.0.0.1:5000/api/v1/resources/orders/dailyOrders/2010-10-10/</a
      >
      <br />
    </p>

    <p>
      - sales data for date range:
      <br />http://127.0.0.1:5000/api/v1/resources/orders/dailyOrders/start/end/
      <br />example usage
      <a
        href="http://127.0.0.1:5000/api/v1/resources/orders/dailyOrders/2010-10-10/2011-10-10/"
        >http://127.0.0.1:5000/api/v1/resources/orders/dailyOrders/2010-10-10/2011-10-10/</a
      >
      <br />
    </p>

    <p>
      Orders data is available for date range: {{ ORDERS_START }} -
      {{ ORDERS_END }}
    </p>
    <p>
      Note, that there is a limit for requests: {{ DEFAULT_LIMIT }} per user.
      Cache timeout is set to {{ CACHE_DEFAULT_TIMEOUT }} seconds.
    </p>
  </v-container>
</template>
<script>
export default {
  name: "instructionDisplay",
  //   props: {
  //     msg: String
  //   }
  data() {
    return {
      switch1: true,
      date1: "2010-10-10",
      date2: "2010-10-11",
      BAD_REQUEST: 400,
      NO_DATA_FOUND: 404,
      WRONG_DATE_RANGE: 416,
      TOO_MANY_REQUESTS: 429,

      ORDERS_START: "2009-01-01",
      ORDERS_END: "2012-12-30",
      DEFAULT_LIMIT: "500 per minute",
      CACHE_DEFAULT_TIMEOUT: 3600,
      NBP_MIN_DATE: "2002-01-02",
      ORDERS_MIN_DATE: "2009-01-01",
      ORDERS_MAX_DATE: "2012-12-30"
    };
  }
};
</script>
