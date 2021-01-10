<style scoped>
.form {
  width: 50%;
}

.dates-order {
  color: red;
  font-size: 12px;
}
.request-failed {
  color: red;
}
</style>

<template>
  <v-container>
    <v-row class="text-center">
      <v-col align="center" size="12">
        <v-form class="form" v-model="valid" ref="form">
          <v-select
            :items="items"
            label="Choose request data"
            v-model="selectedRequest"
            @change="resetData"
            required
            :rules="dataRules"
          ></v-select>

          <div v-if="selectedRequest === 'rates'" class="rates">
            <h3 align="left">Choose the endpoint</h3>
            <v-select
              :items="rates"
              label="Select option"
              v-model="selectedEndpoint"
              required
              :rules="dataRules"
            ></v-select>
            <v-slider
              v-model="days"
              v-if="selectedEndpoint === 'Last N'"
              min="1"
              max="100"
              thumb-label
              label="N"
              required
              :rules="dataRules"
            ></v-slider>
          </div>

          <div v-if="selectedRequest === 'sales'" class="sales">
            <h3 align="left">Choose the endpoint</h3>
            <v-select
              :items="sales"
              label="Select option"
              v-model="selectedEndpoint"
              required
              :rules="dataRules"
            ></v-select>
          </div>

          <DatePicker
            v-if="selectedEndpoint === 'Day' || selectedEndpoint === 'Period'"
            v-on:setDate="startDate = $event"
            label="Choose date"
            :rules="dataRules"
          ></DatePicker>
          <DatePicker
            v-if="selectedEndpoint === 'Period'"
            v-on:setDate="endDate = $event"
            label="Choose end date"
            :rules="dataRules"
          ></DatePicker>
          <p class="dates-order" v-if="!datesOrdered">End date must be smaller than start date!</p>
          <v-btn color="primary" v-on:click="submitForm">Submit Form</v-btn>
          <p class="request-failed ma-4" v-if="requestError">No data for given parameters!</p>
        </v-form>
      </v-col>

    </v-row>
      <v-row align="center" class="ma-4">
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-header>Response</v-expansion-panel-header>
            <v-expansion-panel-content><pre>{{response | prettify}}</pre></v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-row>
  </v-container>
</template>

<script>
import DatePicker from "./DatePicker";
import axios from "axios";
export default {
  name: "RequestForm",
  filters: {
    prettify: function(value) {
      return JSON.stringify(JSON.parse(JSON.stringify(value)), null, 2);
      }
    },
  data: () => ({
    selectedRequest: "",
    selectedEndpoint: "",
    startDate: "",
    endDate: "",
    items: ["rates", "sales"],
    rates: ["Day", "Period", "Last N"],
    sales: ["Day", "Period"],
    days: 0,
    response: null,
    valid: true,
    requestError: false,
    datesOrdered: true,
    dataRules: [
      v => !!v || 'Field required'
    ],
  }),
  components: {
    DatePicker,
  },
  methods: {
    resetData() {
      this.selectedEndpoint = "";
      this.startDate = "";
      this.endDate = "";
      this.days = 0;
      this.valid = true;
      this.datesOrdered = true;
    },
    async getDataForRange() {
      await axios.get(`http://127.0.0.1:5000/api/${this.selectedRequest}/${this.startDate}/${this.endDate}`,{responseType: 'json'})
        .then((resp) =>(this.response = resp.data[this.selectedRequest]))
        .catch((e) => {
          this.requestError = true;
          console.log(e);
        });
    },
    async getLastNData() {
      await axios.get(`http://127.0.0.1:5000/api/${this.selectedRequest}/last/${this.days}`,{responseType: 'json'})
        .then((resp) =>(this.response = resp.data[this.selectedRequest]))
        .catch((e) => {
          this.requestError = true;
          console.log(e);
        });
    },
    async getDataForDay() {
      await axios.get(`http://127.0.0.1:5000/api/${this.selectedRequest}/${this.startDate}`,{responseType: 'json'})
        .then((resp) =>(this.response = resp.data))
        .catch((e) => {
          this.requestError = true;
          console.log(e);
        });
    },
    submitForm() {
      if (this.selectedEndpoint === 'Period')
        this.datesOrdered = this.datesValid()
      this.valid = this.$refs.form.validate();
      if (this.valid && this.datesOrdered)
        switch (this.selectedEndpoint) {
          case 'Day': 
            this.getDataForDay();
            break;
          case 'Period':
            this.getDataForRange();
            break;
          case 'Last N':
            this.getLastNData();
            break;
        }
    },
    datesValid() {
      return new Date(this.startDate) <= new Date(this.endDate);
    },
  },
};
</script>
