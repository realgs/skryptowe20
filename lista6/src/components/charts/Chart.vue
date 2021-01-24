<script>
import {Line, mixins} from 'vue-chartjs';
const { reactiveProp } = mixins

export default {
  name: 'LineChart',
  extends: Line,
  mixins: [reactiveProp],
  props: {
    chart_data: Array
  },
  data() {
    return {
      options: {
        responsive: true,
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
  mounted() {
    this.renderChart(this.chart_data, this.options);
  },
};
</script>
