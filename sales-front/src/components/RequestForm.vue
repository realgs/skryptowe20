<style scoped>
.form {
  width: 50%;
}

.dates-order {
  color: red;
  font-size: 12px;
}
</style>

<template>
  <v-container>
    <v-row class="text-center">
      <v-col align="center">
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
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import DatePicker from "./DatePicker";
import axios from "axios";
export default {
  name: "RequestForm",
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
    getDataForRange(dataType) {
      const url = dataType;
      axios
        .get(url)
        .then((resp) => {
          this.response = resp.data;
        })
        .catch((e) => {
          console.log(e);
        });
    },
    getDataForDay() {
      const url = "";
      axios
        .get(url)
        .then((resp) => {
          this.response = resp.data;
        })
        .catch((e) => {
          console.log(e);
        });
    },
    submitForm() {
      if (this.selectedEndpoint === 'Period')
        this.datesOrdered = this.datesValid()
      this.valid = this.$refs.form.validate();
      if (this.valid && this.datesOrdered)
        console.log("Form submitted")
    },
    datesValid() {
      return new Date(this.startDate) <= new Date(this.endDate);
    }
  },
};
</script>
