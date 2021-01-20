<template>
  <div>
    <h2>Make a request to the API</h2>
    <b-alert class="mb-5" variant="danger" :show="showErrors"
      ><ul>
        <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
      </ul></b-alert
    >
    <b-button-group>
      <b-button
        class="mr-2 ml-2"
        @click="
          request = 'rates';
          showErrors = false;
        "
        :class="{ 'btn-success': request === 'rates' }"
        >Request for exchange rates
      </b-button>
      <b-button
        class="mr-2 ml-2"
        @click="
          request = 'sales';
          showErrors = false;
        "
        :class="{ 'btn-success': request === 'sales' }"
        >Request for sales numbers
      </b-button>
    </b-button-group>
    <Rates v-if="this.request === 'rates'" v-on:errors="onErrors($event)" />
    <Sales v-if="this.request === 'sales'" v-on:errors="onErrors($event)" />
  </div>
</template>

<script>
import Rates from "@/components/Rates.vue";
import Sales from "@/components/Sales.vue";

export default {
  name: "Input",
  components: {
    Rates,
    Sales,
  },
  data() {
    return {
      request: null,
      errors: null,
      showErrors: false,
    };
  },
  methods: {
    onErrors(errors) {
      this.errors = errors;
      this.showErrors = errors.length > 0;
    },
  },
};
</script>

<style scoped>
h2 {
  margin: 50px 0 50px;
}
.date-group {
  margin: 50px 25% 50px 25%;
}
ul {
  margin-bottom: 0;
}
</style>
