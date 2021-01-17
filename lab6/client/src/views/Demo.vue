<template>
  <div class="about">
    <h1>Demonstracja działania API</h1>
    <hr />
    <div class="btn-group btn-group-toggle" data-toggle="buttons">
      <label class="btn btn-secondary active">
        <input
          type="radio"
          name="options"
          id="option1"
          autocomplete="off"
          checked
        />
        Notowania
      </label>
      <label class="btn btn-secondary">
        <input type="radio" name="options" id="option2" autocomplete="off" />
        Sprzedaż
      </label>
    </div>
    <rates-table />
  </div>
</template>

<script>
import RatesTable from '../components/RatesTable.vue';

export default {
  components: { RatesTable },
};
</script>
