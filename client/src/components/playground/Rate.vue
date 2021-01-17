<template>
  <div class="rate">
    <h3>Rates</h3>
    <div class="control_panel">
      <select v-model="curr">
        <option v-for="code in codes" :key="code">
          {{ code }}
        </option>
      </select>
      <Date :min-date="new Date(2002, 0, 2)"
            :max-date="new Date(2020, 11, 20)"
            @change="dateData = $event"/>
      <button v-on:click="sendRequest">SEND</button>
    </div>
    <div class="result">
      <Result :res="response" :status="status" :key="requestURL + 'res'"/>
      <LineChart class="chart" :chartdata="chartData" :options="options"
                 v-if="status===200" :key="requestURL + 'chart'"/>
    </div>
  </div>
</template>

<script>
import config from '@/config';
import Date from '@/components/playground/Date.vue';
import Result from '@/components/result/Result.vue';
import axios from 'axios';
import LineChart from '@/components/result/LineChart.vue';

export default {
  name: 'Rate',
  components: {
    LineChart,
    Result,
    Date,
  },
  data() {
    return {
      codes: config.codes,
      curr: config.codes[0],
      dateData: {
        range: {
          start: '2017-05-05',
          end: '2017-06-05',
        },
        date: '2017-05-05',
        isDateRange: false,
      },
      requestURL: '',
      response: [],
      status: 0,
      chartData: {},
      options: {
        maintainAspectRatio: false,
        scales: {
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: '',
            },
            ticks: {
              maxTicksLimit: 15,
              minTicksLimit: 5,
              autoSkip: true,
              beginAtZero: true,
              padding: 10,
            },
          }],
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Date',
            },
            ticks: {
              maxTicksLimit: 15,
              autoSkip: true,
            },
          }],
        },
      },
    };
  },
  methods: {
    sendRequest() {
      let requestURL = config.apiPath.concat(`/rates/${this.curr}/`);
      requestURL += this.dateData.isDateRange
        ? `${this.dateData.range.start}/${this.dateData.range.end}`
        : `${this.dateData.date}`;
      axios.get(requestURL)
        .then((response) => {
          this.response = response.data;
          this.status = 200;
          this.setChartData(response.data);
        })
        .catch((error) => {
          this.status = error.response.status;
        })
        .finally(() => {
          this.requestURL = requestURL;
        });
    },
    setChartData(resp) {
      const dates = [];
      const mids = [];
      resp.forEach((item) => {
        dates.push(item.dateStr);
        mids.push(item.mid);
      });
      this.options.scales.yAxes[0].scaleLabel.labelString = `${this.curr}/PLN`;
      this.chartData = {
        labels: dates,
        datasets: [{
          label: `${this.curr} rates`,
          data: mids,
          fill: true,
          backgroundColor: '#d3efd1',
          pointBackgroundColor: '#b0eeab',
          pointBorderColor: '#29f154',
          lineTension: 0,
        }],
      };
    },
  },
};
</script>

<style lang="scss" scoped>
.rate {
  background-color: white;
  margin: 20px auto;
  border-radius: 10px;
  box-shadow: 3px 3px 10px gray;
  width: 80%;
  max-width: 1200px;
  padding: 10px 30px;
}

.control_panel, .result {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.control_panel * {
  margin: auto 2px;
}

.chart {
  max-height: 700px;
  min-width: 600px;
  width: 55%;
}
</style>
