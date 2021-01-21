<template>
  <div>
    <div class="hello">
      <h1>BikeStores</h1>
      <p>
        BikeStores is an API that provides information about the US dollar
        exchange rates starting from the year 2002 onwards and sales in a bike
        shop over a period of time from
        <span class="oneline">2016-01-01</span> to
        <span class="oneline">2018-12-28</span>.
      </p>
      <p>
        The API uses route /api for all requests. The date format used in both
        requests and responses is <em class="oneline">YYYY-MM-DD</em>. Using
        format <em class="oneline">YYYY-M-D</em> in requests is also acceptable.
      </p>
      <p>You can test the API by going to the page below:</p>
      <a href="/request">Make a request to the API</a>
    </div>

    <div class="desc">
      <h2>API endpoints</h2>
      <h4>/api/rates/&lt;date_start&gt;/&lt;date_end&gt;</h4>
      <p>
        Provides PLN to USD exchange rate for the time period between
        <code>date_start</code> and <code>date_end</code> (inclusive). The
        responses will be cached for <span class="oneline">5 minutes.</span>
      </p>
      The API server can respond with:
      <ul>
        <li>
          A dictionary with one key <code>rates</code>, containing an ordered
          list of dictionaries for every day of the time period specified in the
          request. The dictionary for a single day contains three keys:
        </li>
        <ul>
          <li>
            <code>date</code>:
            <em>string of format <span class="oneline">YYYY-MM-DD</span></em> -
            date on which the exchange rate was determined
          </li>
          <li>
            <code>rate</code>: <em>double</em> - exchange rate from PLN to USD
          </li>
          <li>
            <code>interpolated</code>: <em>boolean</em> - whether the exchange
            rate was int
          </li>
          erpolated based on previous values
        </ul>
        <li>Bad request if the date format is invalid</li>
        <li>
          Bad request if the <code>date_start</code> is earlier than
          <code>date_end</code>
        </li>
        <li>Bad request if the time period is longer than 366 days</li>
        <li>Too many requests if the user made more requests than:</li>
        <ul>
          <li>1 per second</li>
          <li>10 per minute</li>
          <li>100 per hour</li>
        </ul>
        <li>
          Message stating that the data was not found if the time period starts
          before <span class="oneline">2002-01-02</span> or ends after the day
          that the database was last updated.
        </li>
      </ul>

      <h4>/api/rates/&lt;date&gt;</h4>
      <p>Redirects to <em>/api/rates/&lt;date&gt;/&lt;date&gt;</em></p>

      <h4>/api/sales/&lt;date_start&gt;/&lt;date_end&gt;</h4>
      <p>
        Provides PLN to USD exchange rate for the time period between
        <code>date_start</code> and <code>date_end</code> (inclusive). The
        responses will be cached for 10 minutes.
      </p>
      The API server can respond with:
      <ul>
        <li>
          A dictionary with one key <code>sales</code>, containing an ordered
          list of dictionaries for every day of the time period specified in the
          request. The dictionary for a single day contains three keys:
        </li>
        <ul>
          <li>
            <code>date</code>:
            <em>string of format <span class="oneline">YYYY-MM-DD</span></em> -
            date on which the sales were recorded
          </li>
          <li>
            <code>original_sales</code>: <em>double</em> - value of total sales
            made on a given day in USD
          </li>
          <li>
            <code>exchanged_sales</code>: <em>double</em> - value of total sales
            made on a given day, converted to PLN using the exchange rate from
            /api/rates route for a given day
          </li>
        </ul>
        <li>Bad request if the date format is invalid</li>
        <li>
          Bad request if the <code>date_start</code> is earlier than
          <code>date_end</code>
        </li>
        <li>Bad request if the time period is longer than 366 days</li>
        <li>Too many requests if the user made more requests than:</li>
        <ul>
          <li>1 per second</li>
          <li>10 per minute</li>
        </ul>
        <li>
          Message stating that the data was not found if the time period starts
          before <span class="oneline">2016-01-01</span> or ends after
          <span class="oneline">2018-12-28</span>.
        </li>
      </ul>

      <h4>/api/sales/&lt;date&gt;</h4>
      <p>Redirects to <em>/api/sales/&lt;date&gt;/&lt;date&gt;</em></p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ApiDescription",
};
</script>

<style scoped>
h1 {
  margin: 40px 0 40px;
  font-weight: bold;
}
a {
  font-size: 1.25em;
}
h2 {
  text-align: center;
  margin: 100px 0 40px;
}
h4 {
  margin: 30px 0 30px;
}
a {
  color: #349fe6;
}
code {
  font-size: 1.1em;
  color: slateblue;
}
.hello {
  margin: 0 30% 0 30%;
  text-align: justify;
  text-align-last: center;
}
.desc {
  text-align: justify;
  margin: 0 20% 100px 20%;
}
.oneline {
  white-space: nowrap;
}
</style>
