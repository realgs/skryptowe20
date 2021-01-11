<template>
    <v-row class="text-center">
        <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold ma-4">
          Available endpoints
        </h1>
        <p>All available endpoints are listed below. For full documentation visit <a href="https://github.com/Silkypaladin/skryptowe20/tree/L5">github docs</a>.</p>
      </v-col>

      <v-col class="mb-5" cols="12">
          <h3 class="ma-3">Rates endpoints</h3>
          <v-expansion-panels>
              <v-expansion-panel>
                  <v-expansion-panel-header>Get rates for day</v-expansion-panel-header>
                  <v-expansion-panel-content>
                     <p>Returns json data about an exchange rate for a given day.</p>
                     <h3>URL</h3>
                     <p>/api/rates/:date, date format: <strong>YYYY-mm-dd</strong></p>
                  </v-expansion-panel-content>
              </v-expansion-panel>

               <v-expansion-panel>
                  <v-expansion-panel-header>Get rates for period</v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <p>Returns json data about exchange rates for a given period. Maximum date span is 366 days.</p>
                    <h3>URL</h3>
                    <p>/api/rates/:start_date/:end_date, start_date and end_date format: <strong>YYYY-mm-dd</strong></p>
                  </v-expansion-panel-content>
              </v-expansion-panel>

              <v-expansion-panel>
                  <v-expansion-panel-header>Get last n rates</v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <p>Returns json data about last n rates. Maximum amount of days is 100.</p>
                    <h3>URL</h3>
                    <p>/api/rates/last/:days, days: and integer form 1 to 100.</p>
                  </v-expansion-panel-content>
              </v-expansion-panel>
          </v-expansion-panels>
          <h3 class="ma-3">Sales endpoints</h3>
          <v-expansion-panels>
              <v-expansion-panel>
                  <v-expansion-panel-header>Get sales for day</v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <p>Returns json data about sales for a given day.</p>
                    <h3>URL</h3>
                    <p>/api/sales/:date, date format: <strong>YYYY-mm-dd</strong></p>
                  </v-expansion-panel-content>
              </v-expansion-panel>

               <v-expansion-panel>
                  <v-expansion-panel-header>Get sales for period</v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <p>Returns json data about sales data for a given period. Maximum date span is 366 days.</p>
                    <h3>URL</h3>
                    <p>/api/sales/:start_date/:end_date, start_date and end_date format: <strong>YYYY-mm-dd</strong></p>
                  </v-expansion-panel-content>
              </v-expansion-panel>
          </v-expansion-panels>

      </v-col>
    </v-row>
</template>

<script>
export default {
    name: "Docs",
}
</script>
