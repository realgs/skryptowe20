import React, { Component } from "react";
import Badge from "react-bootstrap/Badge";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Table from "react-bootstrap/Table";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import Calendar from "react-calendar";
import Chart from "chart.js";
import "react-calendar/dist/Calendar.css";

export default class Exchanges extends Component {
  state = {
    chosenCurrency: "Choose Currency",
    chosenOption: true,
    interpolation: false,
    interpolationResultsPresent: false,
    resultBadgeVariant: "danger",
    resultBadgeText: "No results yet",
    chosenBeginningDate: null,
    chosenEndingDate: null,
    items: null,
    dataset: null,
    labels: null,
    chartReady: false,
    tableReady: false,
    actualChart: null,
  };

  callApi = () => {
    const interAddon = this.state.interpolation ? "/inter/" : "/";
    fetch(
      "/rates" +
        interAddon +
        this.state.chosenCurrency +
        "/" +
        this.state.chosenBeginingDate +
        "/" +
        this.state.chosenEndingDate
    )
      .then((res) => res.json())
      .then((result) => {
        if (Array.isArray(result)) {
          this.setState({
            items: result.map((x) => {
              return x;
            }),
            resultBadgeText: "ok",
            resultBadgeVariant: "success",
            interpolationResultsPresent: this.state.interpolation,
          });
          this.setState({ chartReady: !this.state.chosenOption });
          this.setState({ tableReady: this.state.chosenOption });
          this.createChart();
        } else {
          this.setState({
            resultBadgeText: result.Error,
            resultBadgeVariant: "danger",
          });
        }
      });
  };

  // Components
  infoBadge = (text) => {
    return (
      <h2>
        <Badge className="mx-2 mt-2" variant="primary">
          {text}
        </Badge>
      </h2>
    );
  };

  dropdownCurrencies = () => {
    return (
      <DropdownButton
        className="format m-2"
        id="dropdown-item-button"
        title={this.state.chosenCurrency}
      >
        {this.props.currencies.map((elem, index) => (
          <Dropdown.Item as="button" key={index}>
            <div
              onClick={(e) => this.updateChosenCurrency(e.target.textContent)}
            >
              {elem}
            </div>
          </Dropdown.Item>
        ))}
      </DropdownButton>
    );
  };

  interpolation = () => {
    return (
      <Button
        className="m-2"
        onClick={() => this.updateInterpolation()}
        variant={this.state.interpolation ? "success" : "danger"}
      >
        {this.state.interpolation ? "Interpolation ON" : " Interpolation OFF"}
      </Button>
    );
  };

  doubleCalendars = () => {
    return (
      <div className="d-flex">
        <div className="d-block mr-5">
          <h4 style={{ color: "white" }}>
            <span
              className="badge m-2 bg-primary d-flex"
              style={{ justifyContent: "center" }}
            >
              Choose Beginning Date:
            </span>
          </h4>
          <Calendar
            className="m-2"
            onChange={(value) => this.updateChosenBeginingDate(value)}
          />
        </div>
        <div className="d-block">
          <h4 style={{ color: "white" }}>
            <span
              className="badge m-2 bg-primary d-flex "
              style={{ justifyContent: "center" }}
            >
              Choose Ending Date:
            </span>
          </h4>
          <Calendar
            className="m-2"
            onChange={(value) => this.updateChosenEndingDate(value)}
          />
        </div>
      </div>
    );
  };

  tryButton = () => {
    return (
      <div className="m-2">
        <Dropdown as={ButtonGroup}>
          <Button onClick={this.callApi} variant="primary">
            {"Click here to generate: " +
              (this.state.chosenOption ? "Table" : "Graph")}
          </Button>
          <Dropdown.Toggle split variant="primary" id="dropdown-custom-2" />
          <Dropdown.Menu className="table-or-graph">
            <Dropdown.Item eventKey="1">
              <div
                onClick={() => {
                  this.setState({ chosenOption: 1 });
                  this.setState({ chartReady: false });
                }}
              >
                Table
              </div>
            </Dropdown.Item>
            <Dropdown.Item eventKey="2">
              <div
                onClick={() => {
                  this.setState({ chosenOption: 0 });
                  this.setState({ tableReady: false });
                }}
              >
                Graph
              </div>
            </Dropdown.Item>
          </Dropdown.Menu>
        </Dropdown>
      </div>
    );
  };

  resultBadge = () => {
    return (
      <h2 style={{ color: "white" }}>
        <Badge className="m-2" variant={this.state.resultBadgeVariant}>
          {this.state.resultBadgeText}
        </Badge>
      </h2>
    );
  };

  exchangeRatesTable = () => {
    if (
      this.state.items !== null &&
      this.state.chosenOption &&
      this.state.tableReady
    ) {
      return (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Date</th>
              <th scope="col">Exchange Rate (PLN)</th>
              {this.state.interpolationResultsPresent && (
                <th scope="col">Interpolation</th>
              )}
            </tr>
          </thead>
          <tbody>
            {this.state.items.map((elem, index) => (
              <tr key={index}>
                <th scope="row">{index + 1}</th>
                <td>{elem.date}</td>
                <td>{elem.rate}</td>
                {this.state.interpolationResultsPresent && (
                  <td>{elem.interpolated}</td>
                )}
              </tr>
            ))}
          </tbody>
        </Table>
      );
    }
    return null;
  };

  footer = () => {
    return (
      <div className="card-footer border-primary text-muted">
        More info at my <a href={this.props.github}>github page</a>
      </div>
    );
  };

  createChart = () => {
    if (this.state.items != null && !this.state.chosenOption) {
      var labels = [];
      var dataset = [];
      this.state.items.forEach((x) => {
        dataset.push(x.rate);
        labels.push(x.date);
      });
      if(this.state.actualChart !== null){
        this.state.actualChart.destroy();
      }
      
      if (this.state.items.length === 1) {
        this.barChart(labels, dataset);
      } else {
        this.lineChart(labels, dataset);
      }
    }
  };

  barChart = (labels, dataset) => {
    var ctx = document.getElementById("exchangeChart").getContext("2d");
    var chart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: this.state.chosenCurrency,
            backgroundColor: "blue",
            data: dataset,
            barThickness: 16,
          },
        ],
      },
      options: {
        scales: {
          yAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: "PLN",
              },
            },
          ],
        },
      },
    });
    this.setState({actualChart : chart})
  };

  lineChart = (labels, dataset) => {
    var ctx = document.getElementById("exchangeChart").getContext("2d");
    var chart = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: this.state.chosenCurrency,
            borderJoinStyle: "miter",
            pointBorderColor: "transparent",
            pointBackgroundColor: "transparent",
            backgroundColor: "transparent",
            borderColor: "blue",
            data: dataset,
          },
        ],
      },
      options: {
        scales: {
          xAxes: [
            {
              ticks: {
                maxTicksLimit: 20.1,
                labelString: "PLN",
              },
            },
          ],
        },
      },
    });
    this.setState({actualChart : chart})
  };

  render() {
    return (
      <div className="container">
        <div className="card border-primary mb-5">
          <div className="card-header border-primary">
            <div>{this.infoBadge("You Are Now At Exchange Rates Page")}</div>
          </div>
          <div className="card-body">
            <div className="d-flex">
              <div>{this.dropdownCurrencies()}</div>
              <div>{this.interpolation()}</div>
            </div>
            <div>{this.doubleCalendars()}</div>
            <div className="d-flex">
              <div>{this.tryButton()}</div>
              <div>{this.resultBadge()}</div>
            </div>
            <div>{this.exchangeRatesTable()}</div>
            {this.state.chartReady && <canvas id="exchangeChart"></canvas>}
          </div>
          <div>{this.footer()}</div>
        </div>
      </div>
    );
  }

  // Utils
  updateChosenCurrency = (value) => {
    this.setState({ chosenCurrency: value });
  };

  updateInterpolation(event) {
    this.setState({ interpolation: !this.state.interpolation });
  }

  updateChosenBeginingDate = (value) => {
    this.setState({ chosenBeginingDate: this.formatDate(value) });
  };

  updateChosenEndingDate = (value) => {
    this.setState({ chosenEndingDate: this.formatDate(value) });
  };

  formatDate = (date) => {
    var d = new Date(date),
      month = "" + (d.getMonth() + 1),
      day = "" + d.getDate(),
      year = d.getFullYear();
    if (month.length < 2) month = "0" + month;
    if (day.length < 2) day = "0" + day;
    return [year, month, day].join("-");
  };
}
