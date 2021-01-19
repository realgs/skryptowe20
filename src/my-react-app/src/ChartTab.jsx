import React, { Component } from "react";
import ApiForm from "./Common/ApiForm";
import Chart from "./Chart/Chart";

class ChartsTab extends Component {
  optionalChart() {
    if (this.props.data.length > 0) {
      return (
        <Chart
          labels={this.props.labels}
          label={this.props.label}
          data={this.props.data}
        />
      );
    }
  }
  render() {
    return (
      <React.Fragment>
        <ApiForm
          fetchSales={this.props.fetchSales}
          fetchCurrency={this.props.fetchCurrency}
        />
        {this.optionalChart()}
      </React.Fragment>
    );
  }
}

export default ChartsTab;
