<template>
  <v-container>
    <v-row class="justify-center" mb-6>
      <v-switch
        v-model="isRates"
        @change="reset"
        :label="`${isRates ? 'Currency rates' : 'Sales'}`"
      />
    </v-row>
    <v-row align="center">
      <myDatePicker @pick-date="changeDates" :isRates="isRates" />
    </v-row>
    <v-row class="justify-center" mt-10 mb-10>
      <v-btn @click="getData" mr-10> Show data</v-btn>
    </v-row>
    <v-col>
      <GChart
        v-show="showCh"
        full-width
        mt-10
        type="ColumnChart"
        :data="chartData"
      />
    </v-col>

    <v-layout justify-center justify-content-center mt-10>
      <v-simple-table fixed-header>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-center">
                Date
              </th>
              <th class="text-center">
                {{ isRates ? "rate" : "sales in USD" }}
              </th>
              <th class="text-center">
                {{ isRates ? "intrpolated" : "sales in PLN" }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in fetchedData" :key="item.name">
              <td class="text-right">{{ index }}</td>
              <td class="text-right">
                {{ isRates ? item.rate : item.orders_cost_in_usd + " $" }}
              </td>
              <td class="text-right">
                {{
                  isRates ? item.interpolated : item.orders_cost_in_pln + " zl"
                }}
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-layout>
  </v-container>
</template>
<script>
import myDatePicker from "./MyDatePicker";
import axios from "axios";
import { GChart } from "vue-google-charts";

export default {
  name: "settingsDisplay",
  data() {
    return {
      dates: [],
      date1: "",
      date2: "",
      isRates: false,
      fetchedData: [],
      chartData: [],
      newDates: [],
      showChart: false
    };
  },
  components: {
    myDatePicker,
    GChart
  },
  methods: {
    reset(){
      this.fetchedData=[]
      this.dates=[]
      this.chartData=[]
      this.showChart=false
    },
    getData() {
      if(this.dates.length == 2){
        if(Date.parse(this.dates[1]) < Date.parse(this.dates[0])){
          this.date1 = this.dates[1]
          this.date2 = this.dates[0]
        }
        else{
          this.date1 = this.dates[0]
          this.date2 = this.dates[1]
        }
      }
      else{
        this.date1 = this.dates[0]
        this.date2 = this.dates[0]
      }
      const path = this.isRates
        ? "http://127.0.0.1:5000/api/v1/resources/rates/usd/" +
          this.date1 +
          "/" +
          this.date2 +
          "/"
        : "http://127.0.0.1:5000/api/v1/resources/orders/dailyOrders/" +
          this.date1 +
          "/" +
          this.date2 +
          "/";
      axios
        .get(path)
        .then(res => {
          console.log(path);
          console.log(res.data);
          this.fetchedData = res.data;
          this.jsonToTable();
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    changeDates(newDates) {
      this.dates = newDates;
      console.log(this.dates);
    },
    jsonToTable() {
      this.newDates = Object.keys(this.fetchedData);
      this.chartData = [];
      if (this.isRates) {
        this.chartData.push(["date", "rate"]);
        for (var i = 0; i < Object.keys(this.fetchedData).length; i++) {
          this.chartData.push([
            this.newDates[i],
            this.fetchedData[this.newDates[i]].rate
          ]);
        }
      } else {
        this.chartData.push(["date", "sales in usd", "sales in pln"]);
        for (var j = 0; j < Object.keys(this.fetchedData).length; j++) {
          this.chartData.push([
            this.newDates[j],
            this.fetchedData[this.newDates[j]].orders_cost_in_usd,
            this.fetchedData[this.newDates[j]].orders_cost_in_pln
          ]);
        }
      }
      this.showChart = true
    }
  },
  computed: {
    showCh(){
      if(this.showChart && this.dates.length ==2) return true;
      return false
    }
  }
};
</script>
