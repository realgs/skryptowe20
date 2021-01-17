<script>
import { Line } from 'vue-chartjs';

export default {
  name: 'LineChart',
  extends: Line,
  props: {
    chartdata: Object,
    options: Object,
  },
  mounted() {
    this.renderChart(this.chartdata, this.options);
  },
};
</script>
