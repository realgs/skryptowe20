<style scoped>

.form {
  width: 50%;
}


</style>

<template>
  <v-container>
    <v-row class="text-center">
      <!-- <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">
          Welcome to SalesMan
        </h1>

        <p class="subheading font-weight-regular">
          An amazing app with simple UI,
          <br/>making SalesMan API communication quick and easy.
        </p>
      </v-col>

      <v-col class="mb-5" cols="12">
        <h2 class="headline font-weight-bold mb-3">
          Available endpoints
        </h2>

        <v-tabs grow>
          <v-tab>Rates endpoints</v-tab>
          <v-tab>Sales endpoints</v-tab>

          <v-tab-item>
            <v-card flat>
              <v-card-text>
               <h2>Get rates for day</h2>
               <p>Returns json data about an exchange rate for a given day.</p>
               <h3>URL</h3>
               <p>/api/rates/:date, date format: <strong>YYYY-mm-dd</strong></p>

               <h2>Get rates for period</h2>
               <p>Returns json data about exchange rates for a given period. Maximum date span is 366 days.</p>
               <h3>URL</h3>
               <p>/api/rates/:start_date/:end_date, start_date and end_date format: <strong>YYYY-mm-dd</strong></p>

               <h2>Get last n rates</h2>
               <p>Returns json data about last n rates. Maximum amount of days is 100.</p>
               <h3>URL</h3>
               <p>/api/rates/last/:days, days: and integer form 1 to 100.</p>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card flat>
              <v-card-text>
               <h2>Get sales for day</h2>
               <p>Returns json data about sales for a given day.</p>
               <h3>URL</h3>
               <p>/api/sales/:date, date format: <strong>YYYY-mm-dd</strong></p>

               <h2>Get sales for period</h2>
               <p>Returns json data about sales data for a given period. Maximum date span is 366 days.</p>
               <h3>URL</h3>
               <p>/api/sales/:start_date/:end_date, start_date and end_date format: <strong>YYYY-mm-dd</strong></p>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs>
      </v-col> -->
      <v-col align="center">
        <form class="form">
          <v-select
            :items="items"
            label="Choose request data"
            v-model="selectedRequest"
          ></v-select>
          <div v-if="selectedRequest==='rates'" class="rates">
            <h3 align="left">Choose the endpoint</h3>
             <v-select
              :items="rates"
              label="Select option"
              v-model="selectedEndpoint"
            ></v-select>
            <DatePicker></DatePicker>
          </div>
          <div v-if="selectedRequest==='sales'" class="sales">
            <h3 align="left">Choose the endpoint</h3>
             <v-select
              :items="sales"
              label="Select option"
              v-model="selectedEndpoint"
            ></v-select>
          </div>
        </form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import DatePicker from "./DatePicker"
export default {
  name: "HelloWorld",
  data: () => ({
   selectedRequest: "",
   selectedEndpoint: "",
   items: ["rates", "sales"],
   rates: ["Get rates for day", "Get rates for period", "Get last n rates"],
   sales: ["Get sales for day", "Get sales for period"],
   date: '1950-01-01'
  }),
  components: {
    DatePicker
  },
};
</script>


