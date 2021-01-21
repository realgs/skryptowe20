<script>
import {Bar} from 'vue-chartjs';

export default {
  extends: Bar,
  props: {
    chartData: {
      type: Array,
      required: true
    },
    label: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [{
            stacked: true,
          }],
          yAxes: [{
            stacked: true
          }]
        }
      }
    }
  },
  mounted() {
    let dates = this.chartData.map(d => d.date);
    let sales_usd = this.chartData.map(d => d.usd);
    let sales_pln = this.chartData.map(d => d.pln);

    this.renderChart({
          labels: dates,
          datasets: [{
            label: 'total in USD',
            data: sales_usd,
            backgroundColor: '#f87979',
            barPercentage: 1,
          },
            {
              label: 'total in PLN',
              data: sales_pln,
              backgroundColor: '#3D5B96',
              barPercentage: 1,
            }]
        },
        this.options
    );
  }
}
</script>