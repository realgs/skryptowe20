import Chart from 'chart.js'
import React from 'react'

export default class LineChart extends React.Component {
  constructor(props) {
    super(props);
    this.chartRef = React.createRef();
  }

  componentDidUpdate() {
    this.myChart.data.labels = this.props.data.map(d => d.date);
    this.myChart.data.datasets[0].data = this.props.data.map(d => d.value);
    this.myChart.data.datasets[0].label = this.props.title;
    this.myChart.update();
  }

  componentDidMount() {
    this.myChart = new Chart(this.chartRef.current, {
      type: 'line',
      options: {
        scales: {
          xAxes: [
            {
              type: 'time',
            }
          ],
          yAxes: [
            {
              ticks: {
              }
            }
          ]
        }
      },
      data: {
        labels: this.props.data.map(d => d.date),
        datasets: [{
          label: this.props.title,
          data: this.props.data.map(d => d.value),
          fill: 'none',
          backgroundColor: this.props.color,
          pointRadius: 2,
          borderColor: this.props.color,
          borderWidth: 1,
          lineTension: 0
        }]
      }
    });
  }

  render() {
    return <canvas ref={this.chartRef} />;
  }
}
