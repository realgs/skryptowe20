import React, { Component } from "react";
import { Line, Bar } from "react-chartjs-2";
import { MDBContainer } from "mdbreact";

class Chart extends Component {
  getChartDependingOnInput() {
    const length = this.props.data.length;
    if (length > 1) {
      return (
        <Line
          data={{
            labels: this.props.labels,
            datasets: [
              {
                label: this.props.label,
                fill: true,
                lineTension: 0.3,
                backgroundColor: "rgba(184, 185, 210, .3)",
                borderColor: "rgb(35, 26, 136)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgb(35, 26, 136)",
                pointBackgroundColor: "rgb(255, 255, 255)",
                pointBorderWidth: 10,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgb(0, 0, 0)",
                pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: this.props.data,
              },
            ],
          }}
          options={{
            responsive: true,
            legend: {
              display: false,
            },
          }}
        />
      );
    } else if (length === 1) {
      return (
        <Bar
          data={{
            labels: this.props.labels,
            datasets: [
              {
                label: this.props.label,
                data: this.props.data,
                backgroundColor: ["#00008b"],
                borderWidth: 2,
                borderColor: ["rgba(0, 0, 0, 1)"],
              },
            ]
          }}
          options={{
            responsive: true,
            legend: {
              display: false,
            },
            maintainAspectRatio: true,
            scales: {
              xAxes: [
                {
                  barPercentage: 0.2,
                  gridLines: {
                    display: true,
                    color: "rgba(0, 0, 0, 0.1)",
                  },
                },
              ],
              yAxes: [
                {
                  gridLines: {
                    display: true,
                    color: "rgba(0, 0, 0, 0.1)",
                  },
                  ticks: {
                    beginAtZero: true,
                  },
                },
              ],
            },
          }}
        />
      );
    }
  }

  render() {
    return <MDBContainer>{this.getChartDependingOnInput()}</MDBContainer>;
  }
}

export default Chart;
