<template>
  <div>
    <div>
      <b-form @submit="onSubmit">
        <b-form-group
          class="date-group"
          label="Date of sales"
          label-for="datepicker"
        >
          <b-form-datepicker
            id="datepicker"
            v-model="form.date"
            placeholder="Choose date of sales"
            locale="en"
            :min="min"
            :max="max"
            show-decade-nav
            today-button
          ></b-form-datepicker>
        </b-form-group>

        <b-button type="submit" variant="primary">Send request</b-button>
      </b-form>
    </div>
    <div class="sales-results" v-if="results != null">
      <p>On the day {{ results.date }}</p>
      <p>Total sales revenue was {{ results.original_total }} USD</p>
      <p>
        Which is about {{ results.exchanged_total }} PLN using the average
        exchange rate on that day
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Sales",
  data() {
    return {
      form: {
        date: null,
      },
      min: new Date(2016, 0, 1),
      max: new Date(2018, 11, 28),
      results: null,
    };
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      const errors = [];

      if (this.form.date == null) {
        errors.push("The date is empty");
        this.$emit("errors", errors);
        return;
      }

      await fetch(`/api/sales/${this.form.date}`)
        .then((response) => response.json())
        .then((data) => (this.results = data.sales));
    },
  },
};
</script>

<style scoped>
.date-group {
  margin: 50px 25% 50px 25%;
}
.sales-results {
  margin: 50px 50px 50px 50px;
}
</style>
