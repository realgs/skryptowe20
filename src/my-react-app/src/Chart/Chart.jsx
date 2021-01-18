import React, { Component } from "react";
import { Line } from "react-chartjs-2";
import { MDBContainer } from "mdbreact";

class Chart extends Component {
  render() {
    return (
      <MDBContainer>
        <h3 className="mt-5">Currency exchange rate chart</h3>
        <Line
          data={{
            labels: this.props.labels,
            datasets: [
              {
                label: "Exchange rate",
                fill: true,
                lineTension: 0.3,
                backgroundColor: "rgba(225, 204,230, .3)",
                borderColor: "rgb(205, 130, 158)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgb(205, 130,1 58)",
                pointBackgroundColor: "rgb(255, 255, 255)",
                pointBorderWidth: 10,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgb(0, 0, 0)",
                pointHoverBorderColor: "rgba(220, 220, 220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: this.props.data,
              },
            ],
          }}
          options={{ responsive: true }}
        />
      </MDBContainer>
    );
  }
}

export default Chart;
