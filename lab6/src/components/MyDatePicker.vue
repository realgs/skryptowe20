<template>
  <v-date-picker
    full-width
    @input="pickDate"
    v-model="dates"
    :min="minDate"
    :max="maxDate"
    range
    class="mt-4"
  ></v-date-picker>
</template>
<script>
var yesterday = new Date();
yesterday.setDate(yesterday.getDate() - 1);
export default {
  name: "myDatePicker",
  data() {
    return {
      maxRatesDate: yesterday.toISOString().slice(0, 10),
      maxSalesDate: "2012-12-30",
      minRatesDate: "2002-01-02",
      minSalesDate: "2009-01-01",
      dates: [],
      fetchedData: []
    };
  },
  props: {
    isRates: {
      type: Boolean,
      required: true
    }
  },
  computed: {
    minDate() {
      return this.isRates ? this.minRatesDate : this.minSalesDate;
    },
    maxDate() {
      return this.isRates ? this.maxRatesDate : this.maxSalesDate;
    }
  },
  watch: {
    isRates() {
      this.dates = [];
    }
  },
  methods: {
    pickDate() {
      this.$emit("pick-date", this.dates);
    }
  }
};
</script>
