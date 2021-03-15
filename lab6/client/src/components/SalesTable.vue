<template>
  <div>
    <br />
    <h5>1. Wybierz zakres sprzedaży</h5>
    <br />
    <br />
    <vue-slider
      v-model="value"
      :enable-cross="false"
      :tooltip="'always'"
      :min="sliderMin"
      :max="sliderMax"
      :marks="sliderMarks"
    />
    <br />
    <br />
    <h5>2. Potwierdź swój wybór</h5>
    <button type="button" class="btn btn-primary" @click="onApply">
      Potwierdź
    </button>
    <br />
    <div v-if="showChart" class="chart">
      <line-chart
        :chart-data="datacollection"
        :options="chartOptions"
      ></line-chart>
    </div>
    <div>
      <table id="table" v-if="showTable" class="table table-hover">
        <thead>
          <tr>
            <th scope="col">Data</th>
            <th scope="col">Wartość sprzedaży oryginalna [w USD]</th>
            <th scope="col">Wartość sprzedaży po przeliczeniu [w PLN]</th>
            <th scope="col">Przelicznik</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(sale, index) in sales" :key="index">
            <td>{{ sale.date }}</td>
            <td>{{ sale.original_value }}</td>
            <td>{{ sale.exchanged_value }}</td>
            <td>{{ sale.exchange_rate }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <hr />
  </div>
</template>

<script>
import VueSlider from 'vue-slider-component';
import axios from 'axios';
import LineChart from './LineChart';
import config from '../config';

export default {
  components: {
    VueSlider,
    LineChart,
  },
  data() {
    return {
      value: [4, 10],
      sliderMin: 1,
      sliderMax: 31,
      sliderMarks: {
        1: '2017-10-1',
        10: '2017-10-10',
        20: '2017-10-20',
        31: '2017-10-31',
      },
      showTable: false,
      showChart: false,
      sales: [],
      datacollection: null,
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
      },
    };
  },
  methods: {
    async onApply() {
      await this.getSales(this.value[0], this.value[1]);
      this.fillData();
      this.showChart = this.sales.length > 1;
      this.showTable = true;
    },
    fillData() {
      this.datacollection = {
        labels: this.sales.map((a) => a.date),
        datasets: [
          {
            label: 'Sprzedaż w USD',
            backgroundColor: '#3f9ecc',
            data: this.sales.map((a) => a.original_value),
          },
          {
            label: 'Sprzedaż w PLN',
            backgroundColor: '#7fc8eb',
            data: this.sales.map((a) => a.exchanged_value),
          },
        ],
      };
    },
    getSales(firstDay, lastDay) {
      const startDate = `2017-10-${firstDay}`;
      const endDate = `2017-10-${lastDay}`;

      const path = `http://${config.backendAddress}:5000/api/v1/sales/sum/range/${startDate}/${endDate}`;
      return axios.get(path).then((res) => {
        this.sales = res.data;
      });
    },
  },
};
</script>

<style scoped>
#currencySelect {
  max-width: 15em;
}
#table {
  margin-top: 10px;
}
</style>
