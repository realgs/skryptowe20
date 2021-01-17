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
    <h5>3. Potwierdź swój wybór</h5>
    <button type="button" class="btn btn-primary" @click="onApply">
      Potwierdź
    </button>
    <br />
    <br />
    <table v-if="showTable" class="table table-hover">
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
</template>

<script>
import VueSlider from 'vue-slider-component';
import axios from 'axios';

export default {
  components: {
    VueSlider,
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
      sales: [],
    };
  },
  methods: {
    onApply() {
      this.getSales(this.value[0], this.value[1]);
      this.showTable = true;
    },
    getSales(firstDay, lastDay) {
      this.sales = [];
      for (let i = firstDay - 1; i < lastDay; i += 1) {
        const datetime = `2017-10-${i + 1}`;
        const path = `http://localhost:5000/api/v1/sales/sum/${datetime}`;
        axios
          .get(path)
          .then((res) => {
            this.sales.push(res.data);
          })
          .catch((error) => {
            this.sales.push({
              date: datetime,
              original_value: 'NO SALES',
              exchanged_value: 'NO SALES',
              exchange_rate: '',
            });
            // eslint-disable-next-line
            console.error(error);
          });
        // eslint-disable-next-line
        console.info(this.sales);
      }
    },
  },
};
</script>

<style scoped>
#currencySelect {
  max-width: 15em;
}
</style>
