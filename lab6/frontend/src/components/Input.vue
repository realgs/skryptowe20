<template>
  <div>
    <div>
      <h2>Make a request to the API</h2>
      <b-alert class="mb-5" variant="danger" :show="errors != null"
        ><ul>
          <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
        </ul></b-alert
      >
      <b-button-group>
        <b-button
          class="mr-2 ml-2"
          @click="onRates()"
          :class="{ 'btn-success': request === 'rates' }"
          >Request for exchange rates
        </b-button>
        <b-button
          class="mr-2 ml-2"
          @click="onSales()"
          :class="{ 'btn-success': request === 'sales' }"
          >Request for sales numbers
        </b-button>
      </b-button-group>
    </div>
    <div v-if="request">
      <div>
        <b-form @submit="onSubmit">
          <b-form-group
            class="date-group"
            label="Starting date"
            label-for="starting-datepicker"
          >
            <b-form-datepicker
              id="starting-datepicker"
              v-model="form.start"
              placeholder="Choose starting date"
              locale="en"
              :min="min"
              :max="max"
              :state="startingValid"
              @input="checkValidity"
              value-as-date
              show-decade-nav
              today-button
            ></b-form-datepicker>
          </b-form-group>

          <b-form-group
            class="date-group"
            label="Ending date"
            label-for="ending-datepicker"
          >
            <b-form-datepicker
              id="ending-datepicker"
              v-model="form.end"
              placeholder="Choose ending date"
              locale="en"
              :min="min"
              :max="max"
              :state="endingValid"
              @input="checkValidity"
              value-as-date
              show-decade-nav
              today-button
            ></b-form-datepicker>
          </b-form-group>

          <b-button type="submit" variant="primary">Send request</b-button>
        </b-form>
      </div>
      <div>
        <rates-results
          :results="results"
          v-if="request === 'rates'"
        ></rates-results>
        <sales-results
          :results="results"
          v-if="request === 'sales'"
        ></sales-results>
      </div>
    </div>
  </div>
</template>

<script>
import RatesResults from "./RatesResults.vue";
import SalesResults from "./SalesResults.vue";
import moment from "moment";
const format = "YYYY-MM-DD";

export default {
  name: "Input",
  components: {
    RatesResults,
    SalesResults,
  },

  data() {
    return {
      request: null,
      errors: null,
      showErrors: false,
      form: {
        start: null,
        end: null,
      },
      min: null,
      max: null,
      startingValid: null,
      endingValid: null,
      results: null,
    };
  },
  methods: {
    onChange(name, min, max) {
      this.results = null;
      this.request = name;
      this.errors = null;
      this.min = min;
      this.max = max;
      this.checkValidity();
    },
    onRates() {
      this.onChange("rates", new Date(2002, 0, 2), new Date());
    },
    onSales() {
      this.onChange("sales", new Date(2016, 0, 1), new Date(2018, 11, 28));
    },
    async onSubmit(event) {
      event.preventDefault();
      const errors = [];

      if (this.form.start == null) errors.push("Starting date is empty");
      if (this.form.end == null) errors.push("Ending date is empty");

      if (errors.length > 0) {
        this.errors = errors;
        return;
      }

      if (!this.isCorrectOrder())
        errors.push("Ending date is before starting date");
      if (!this.isAcceptableInterval())
        errors.push(
          "The maximum difference between ending and starting date is 366 days."
        );
      if (!this.isBetweenConstraints(this.form.start))
        errors.push("Starting date is out of bounds");
      if (!this.isBetweenConstraints(this.form.end))
        errors.push("Ending date is out of bounds");

      if (errors.length > 0) {
        this.errors = errors;
        return;
      }

      const from = moment(this.form.start).format(format);
      const to = moment(this.form.end).format(format);

      await fetch(`/api/${this.request}/${from}/${to}`)
        .then((response) => response.json())
        .then((data) => {
          if (this.request == "rates") this.results = data.rates;
          else if (this.request == "sales") this.results = data.sales;
          this.errors = null;
        });
    },
    isCorrectOrder() {
      if (this.form.start == null || this.form.end == null) return null;
      return this.form.start <= this.form.end;
    },
    isAcceptableInterval() {
      return moment(this.form.end).diff(moment(this.form.start), "days") <= 366;
    },
    isBetweenConstraints(date) {
      if (this.min == null || this.max == null) return null;
      return date <= this.max && date >= this.min;
    },
    checkValidity() {
      const order = this.isCorrectOrder() && this.isAcceptableInterval();
      this.startingValid = order && this.isBetweenConstraints(this.form.start);
      this.endingValid = order && this.isBetweenConstraints(this.form.end);
    },
  },
};
</script>

<style scoped>
h2 {
  margin: 50px 0 50px;
}
ul {
  margin-bottom: 0;
}
.date-group {
  margin: 50px 25% 50px 25%;
}
</style>
