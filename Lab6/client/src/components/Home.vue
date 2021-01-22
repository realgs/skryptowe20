<template>
     <section class="jumbotron text-center">
        <div class="container">
            <h1 class="jumbotron-heading">PLN to USD rates, sales data display</h1>
            <h3>This website allows to easily browse USD to PLN rates
              and sales from
              <a href="https://github.com/PacktPublishing/Learning-Tableau-10/blob/master/Chapter%2001/Superstore.csv"
                 target="_blank">
                Superstore sample database </a>
              taken from Learning-Tableau course.
              It allows to gain exchange rate and sum of sales summed by day,
            for specified date or for range of dates.</h3>
          <h3>Exchange rates are obtained from <a href="http://api.nbp.pl/" target="_blank">http://api.nbp.pl/</a>,
              supplemented with interpolated rates not found in NBP API.
          </h3>
            <br>
            <p class="lead text-muted">API provides data for dates between:
              2013-01-01 - 2014-12-31</p>
            <p class="lead text-muted">By default cache timeout is set to 100.</p>
            <p class="lead text-muted">By default requests limit is set to 10/s per user.</p>
            <br>
            <p class="lead text-muted">If run locally the API is available at http://127.0.0.1:5000/
            </p>
          <p class="lead text-muted">
            With the use of this API you can obtain:
          </p>
          <ul>
            <li>
            <p class="lead text-muted">PLN to USD exchange rate for specified date:
              http://127.0.0.1:5000/rates/usd/{date}</p>
              <ul>
                <li>
                  <p class="lead text-muted">ex. http://127.0.0.1:5000/rates/usd/2013-01-01</p>
                </li>
              </ul>
            </li>
            <li><p class="lead text-muted">PLN to USD exchange rate for date range:
              http://127.0.0.1:5000/rates/usd/{start_date}/{end_date}</p>
              <ul>
                <li>
                  <p class="lead text-muted">
                    ex. http://127.0.0.1:5000/rates/usd/2013-01-01/2014-12-31
                  </p>
                </li>
              </ul>
            </li>
            <li><p class="lead text-muted">Sales data for specified date:
              http://127.0.0.1:5000/sales/{date}</p><ul>
                <li>
                  <p class="lead text-muted">
                    ex. http://127.0.0.1:5000/sales/2013-01-01
                  </p>
                </li>
              </ul>
            </li>
            <li><p class="lead text-muted">Sales data for date range:
              http://127.0.0.1:5000/sales/{start_date}/{end_date}</p><ul>
                <li>
                  <p class="lead text-muted">
                    ex. http://127.0.0.1:5000/sales/2013-01-01/2014-12-31
                  </p>
                </li>
              </ul>
            </li>
            </ul>
            <br>
            <p class="lead text-muted">For installation instructions and
              full documentation on API visit my github
              <a href="https://github.com/AltiTorie/skryptowe20/tree/Lab5/Lab5" target="_blank">here
              </a></p>
          <p class="lead text-muted">For installation instructions and
              full documentation on this site visit my github
              <a href="https://github.com/AltiTorie/skryptowe20/tree/L6" target="_blank">here
              </a></p>

        </div>
    </section>
</template>

<script>
export default {
  name: 'Home',
};
</script>

<style scoped>

</style>
