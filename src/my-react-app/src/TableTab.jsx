import React, { Component } from "react";
import ApiForm from "./Common/ApiForm";
import { Table } from "react-bootstrap";

class TableTab extends Component {
  optionalTable = () => {
    if (this.props.data.length > 0) {
      return (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>#</th>
              <th>Date</th>
              <th>{this.props.label}</th>
            </tr>
          </thead>
          {this.props.data.map((elem, index) => {
            return <tr>
              <td>{index + 1}</td>
              <td>{this.props.labels[index]}</td>
              <td>{elem}</td>
            </tr>;
          })}
        </Table>
      );
    }
  };

  render() {
    console.log(this.props.data, this.props.labels);
    return (
      <React.Fragment>
        <ApiForm
          fetchSales={this.props.fetchSales}
          fetchCurrency={this.props.fetchCurrency}
        />
        {this.optionalTable()}
      </React.Fragment>
    );
  }
}

export default TableTab;
