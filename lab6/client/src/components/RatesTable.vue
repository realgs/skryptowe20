<template>
  <div>
    <br />
    <h5>1. Wybierz walutę</h5>
    <v-select
      v-model="selectedCurr"
      id="currencySelect"
      :reduce="(name) => name.code"
      :options="currencies"
      :clearable="false"
      label="name"
    ></v-select>
    <br />
    <h5>2. Wybierz zakres notowań</h5>
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
    <h5>3. Potwierdź swój wybór</h5>
    <button type="button" class="btn btn-primary" @click="onApply">
      Potwierdź
    </button>
    <br />
    <br />
    <table v-if="showTable" class="table table-hover">
      <thead>
        <tr>
          <th scope="col">Kod waluty</th>
          <th scope="col">Data</th>
          <th scope="col">Notowanie [w PLN]</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(rate, index) in rates" :key="index">
          <td>{{ rate.code }}</td>
          <td>{{ rate.date }}</td>
          <td>{{ rate.rate }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import VueSlider from 'vue-slider-component';
import vSelect from 'vue-select';
import axios from 'axios';

export default {
  components: {
    VueSlider,
    vSelect,
  },
  data() {
    return {
      value: [4, 10],
      sliderMin: 1,
      sliderMax: 31,
      sliderMarks: {
        1: '2020-10-1',
        10: '2020-10-10',
        20: '2020-10-20',
        31: '2020-10-31',
      },
      showTable: false,
      currencies: [
        { code: 'USD', name: 'Dolar amerykański' },
        { code: 'EUR', name: 'Euro' },
        { code: 'GBP', name: 'Funt brytyjski' },
        { code: 'CHF', name: 'Frank szwajcarki' },
        { code: 'JPY', name: 'Jen japoński' },
        { code: 'CAD', name: 'Dolar kanadyjski' },
        { code: 'THB', name: 'Bat tajski' },
        { code: 'AUD', name: 'Dolar australijski' },
        { code: 'HKD', name: 'Dolar hong-kong' },
      ],
      selectedCurr: 'USD',
      rates: [],
    };
  },
  methods: {
    onApply() {
      this.getRates(this.value[0], this.value[1], this.selectedCurr);
      this.showTable = true;
    },
    getRates(firstDay, lastDay, code) {
      const path = `http://localhost:5000/api/v1/rates/${code}/range/2020-10-${firstDay}/2020-10-${lastDay}?interpolated=1`;
      axios
        .get(path)
        .then((res) => {
          this.rates = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
};
</script>

<style scoped>
#currencySelect {
  max-width: 15em;
}
</style>
