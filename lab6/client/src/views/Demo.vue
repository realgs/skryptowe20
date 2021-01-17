<template>
  <div class="about">
    <h1>Demonstracja działania API</h1>
    <hr />
    <div class="btn-group btn-group-toggle" data-toggle="buttons">
      <label
        class="btn btn-secondary"
        :class="picked == 'rates' ? 'active' : ''"
      >
        <input
          v-model="picked"
          type="radio"
          name="options"
          value="rates"
          id="option1"
          autocomplete="off"
          active
        />
        Notowania
      </label>
      <label
        class="btn btn-secondary"
        :class="picked == 'sales' ? 'active' : ''"
      >
        <input
          v-model="picked"
          type="radio"
          name="options"
          id="option2"
          autocomplete="off"
          value="sales"
        />
        Sprzedaż
      </label>
    </div>
    <div v-if="picked == 'rates'">
      <rates-table />
    </div>
    <div v-else>
      <sales-table />
    </div>
  </div>
</template>

<script>
import RatesTable from '../components/RatesTable.vue';
import SalesTable from '../components/SalesTable.vue';

export default {
  components: { RatesTable, SalesTable },
  data() {
    return {
      picked: 'rates',
    };
  },
  methods: {},
};
</script>
