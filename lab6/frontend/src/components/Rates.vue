<template>
  <div>
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

    <div class="chart">
      <canvas ref="rateChart"></canvas>
    </div>

    <div class="rates-results" v-if="results != null">
      <b-table
        hover
        :items="results"
        head-variant="light"
        outlined
        :fields="fields"
      >
        <template #cell(interpolated)="data">
          <b-form-checkbox
            v-model="data.item.interpolated"
            disabled
          ></b-form-checkbox>
        </template>
      </b-table>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js";
import moment from "moment";
const format = "YYYY-MM-DD";

export default {
  name: "Rates",
  data() {
    return {
      form: {
        start: null,
        end: null,
      },
      min: new Date(2002, 0, 2),
      max: new Date(),
      startingValid: null,
      endingValid: null,
      results: null,
      fields: [
        {
          key: "date",
          label: "Date",
        },
        {
          key: "interpolated",
          label: "Is interpolated?",
        },
        {
          key: "rate",
          label: "USD rate",
        },
      ],
      chart: null,
    };
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      const errors = [];

      if (this.form.start == null) errors.push("Starting date is empty");
      if (this.form.end == null) errors.push("Ending date is empty");

      if (errors.length > 0) {
        this.$emit("errors", errors);
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

      this.$emit("errors", errors);
      if (errors.length > 0) return;

      const from = moment(this.form.start).format(format);
      const to = moment(this.form.end).format(format);

      await fetch(`/api/rates/${from}/${to}`)
        .then((response) => response.json())
        .then((data) => {
          this.results = data.rates;
          this.renderChart();
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
    async renderChart() {
      if (this.chart != null) this.chart.destroy();

      const chartData = {
        labels: [],
        datasets: [
          {
            label: "USD rate [PLN]",
            data: [],
          },
        ],
      };

      for (let item of this.results) {
        chartData.labels.push(item.date);
        chartData.datasets[0].data.push(item.rate);
      }

      await this.$nextTick();
      const ctx = this.$refs.rateChart.getContext("2d");
      this.chart = new Chart(ctx, {
        type: "line",
        data: chartData,
        options: {
          title: {
            display: true,
            text: "USD exchange rate in PLN over time",
          },
          legend: {
            display: false,
          },
          scales: {
            xAxes: [
              {
                scaleLabel: {
                  display: true,
                  labelString: "Date",
                },
              },
            ],
            yAxes: [
              {
                scaleLabel: {
                  display: true,
                  labelString: "PLN value",
                },
              },
            ],
          },
        },
      });
    },
  },
};
</script>

<style scoped>
.date-group {
  margin: 50px 25% 50px 25%;
}
.rates-results {
  margin: 50px 25% 50px 25%;
}
.chart {
  margin: 50px 15% 50px 15%;
}
</style>
