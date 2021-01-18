import React, { Component } from "react";
import ApiForm from "./Common/ApiForm";
import Chart from "./Chart/Chart";

class ChartsTab extends Component {
  render() {
    return (
      <React.Fragment>
        <ApiForm
          fetchSales={this.props.fetchSales}
          fetchCurrency={this.props.fetchCurrency}
        />
        <Chart labels={this.props.labels} data={this.props.data} />
      </React.Fragment>
    );
  }
}

export default ChartsTab;
