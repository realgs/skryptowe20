<template>
  <v-container fill-height>
    <v-row class="mt-2" justify="center">
      <v-col cols="12" sm="6" md="4">
        <v-menu
          ref="start_date"
          v-model="start_date"
          :close-on-content-click="false"
          :return-value.sync="date"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="date"
              label="Pick date"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="date"
            no-title
            scrollable
            show-current="2003-05-05"
            min="2003-05-05"
            max="2005-05-05"
          >
            <v-spacer></v-spacer>
            <v-btn text color="primary" @click="start_date = false">
              Cancel
            </v-btn>
            <v-btn text color="primary" @click="$refs.start_date.save(date)">
              OK
            </v-btn>
          </v-date-picker>
        </v-menu>
      </v-col>
      <v-col cols="12" sm="6" md="4" align="center">
        <v-btn class="ma-2" color="secondary" @click="getData">
          Generate
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <section
          v-if="errored"
          align="center"
          style="color: red; font-size: 18px; font-weight: bold"
        >
          <p>API responded with code {{ error_msg }}</p>
        </section>
        <v-card v-if="active && !errored">
          <v-card-title>
            {{ title }}
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="responseToList"
          ></v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
export default {
  data: () => ({
    date: null,
    response: null,
    errored: false,
    active: false,
    error_msg: "",
    start_date: false,
    headers: null,
    title: "",
    sales_headers: [
      { text: "Date", value: "date" },
      { text: "USD rate", value: "usd_rate" },
      { text: "Sale in PLN", value: "pln_sale_sum" },
      { text: "Sale in USD", value: "usd_sale_sum" },
    ],
    rates_headers: [
      { text: "Date", value: "date" },
      { text: "Interpolated", value: "interpolated" },
      { text: "USD rate", value: "usd_rate" },
    ],
  }),
  props: ["url"],
  computed: {
    responseToList: function () {
      let vals = [this.response];
      return vals;
    },
  },
  methods: {
    async requestForDay() {
      axios
        .get(`http://127.0.0.1:5000/${this.url}/${this.date}`, {
          responseType: "json",
        })
        .then((resp) => (this.response = resp.data))
        .catch((e) => {
          this.errored = true;
          console.log(e);
          this.error_msg = e.response.status + ":   " + e.response.data;
        });
      this.active = "active";
      if (this.url == "rates") {
        this.headers = this.rates_headers;
        this.title = "Rates Data";
      } else if (this.url == "sales") {
        this.headers = this.sales_headers;
        this.title = "Sales Data";
      }
    },
    getData() {
      this.resetDisplay();
      this.requestForDay();
    },
    resetDisplay() {
      this.response = null;
      this.errored = false;
      this.active = false;
      this.error_msg = "";
    },
  },
};
</script>
