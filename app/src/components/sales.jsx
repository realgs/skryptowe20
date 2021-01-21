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

export default class Sales extends Component {
  componentDidMount() {
    var idx = this.props.currencies.findIndex((e) => {
      return e === "USD";
    });
    var currenciesRemastered = [...this.props.currencies];
    currenciesRemastered[idx] = "PLN";
    this.setState({ currencies: currenciesRemastered });
  }

  state = {
    currencies: [],
    chosenCurrency: "Choose Currency",
    chosenOption: true,
    resultBadgeVariant: "danger",
    resultBadgeText: "No results yet",
    chosenBeginingDate: null,
    chosenEndingDate: null,
    items: null,
    dataset: null,
    labels: null,
    chartReady: false,
    tableReady: false,
    actualChart : null,
  };

  callApi = () => {
    fetch(
      "/sales/" +
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
            items: this.setUpItems(result),
          });
          this.setState({
            resultBadgeText: "ok",
            resultBadgeVariant: "success",
            chartReady: !this.state.chosenOption,
            tableReady: this.state.chosenOption,
          });
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
        <Badge className="mx-2 mt-2" variant="warning">
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
        {this.state.currencies.map((elem, index) => (
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

  salesTable = () => {
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
              <th scope="col">USD Sales</th>
              <th scope="col">USD Exchange Rate</th>
              <th scope="col">{this.state.chosenCurrency + " Sales"}</th>
              {this.state.chosenCurrency !== "PLN" && (
                <th scope="col">
                  {this.state.chosenCurrency + " Exchange Rate"}
                </th>
              )}
            </tr>
          </thead>
          <tbody>
            {this.state.items.map((elem) => (
              <tr key={elem.id}>
                <th scope="row">{elem.id}</th>
                <td>{elem.date}</td>
                <td>{elem.usd_sales}</td>
                <td>{elem.usd_rate}</td>
                <td>{elem.sales}</td>
                {this.state.chosenCurrency !== "PLN" && <td>{elem.rate}</td>}
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
      var data_usd = [];
      var data_another = [];
      this.state.items.forEach((x) => {
        data_usd.push(x.usd_sales);
        data_another.push(x.sales);
        labels.push(x.date);
      });
      if(this.state.actualChart !== null){
        this.state.actualChart.destroy();
      }

      if (this.state.items.length === 1) {
        this.barChart(labels, data_usd, data_another);
      } else {
        this.lineChart(labels, data_usd, data_another);
      }
    }
  };

  barChart = (labels, data_usd, data_another) => {
    var ctx = document.getElementById("exchangeChart").getContext("2d");
    var chart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "USD Sales",
            backgroundColor: "blue",
            data: data_usd,
            barThickness: 16,
          },
          {
            label: this.state.chosenCurrency + " Sales",
            backgroundColor: "red",
            data: data_another,
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

  lineChart = (labels, data_usd, data_another) => {
    var ctx = document.getElementById("exchangeChart").getContext("2d");
    var chart = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "USD Sales",
            borderJoinStyle: "miter",
            pointBorderColor: "transparent",
            pointBackgroundColor: "transparent",
            backgroundColor: "transparent",
            borderColor: "blue",
            data: data_usd,
          },
          {
            label: this.state.chosenCurrency + " Sales",
            borderJoinStyle: "miter",
            pointBorderColor: "transparent",
            pointBackgroundColor: "transparent",
            backgroundColor: "transparent",
            borderColor: "red",
            data: data_another,
          },
        ],
      },
      options: {
        scales: {
          xAxes: [
            {
              ticks: {
                maxTicksLimit: 20.1,
                labelString: "Single Unit",
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
            <div>{this.infoBadge("You Are Now At Sales Page")}</div>
          </div>
          <div className="card-body">
            <div className="d-flex">
              <div>{this.dropdownCurrencies()}</div>
            </div>
            <div>{this.doubleCalendars()}</div>
            <div className="d-flex">
              <div>{this.tryButton()}</div>
              <div>{this.resultBadge()}</div>
            </div>
            <div>{this.salesTable()}</div>
            {this.state.chartReady && <canvas id="exchangeChart"></canvas>}
          </div>
          <div>{this.footer()}</div>
        </div>
      </div>
    );
  }

  // Utils
  updateChosenCurrency = (value) => {
    this.setState({
      chosenCurrency: value,
      tableReady: false,
      chartReady: false,
      resultBadgeText: "No results yet",
      resultBadgeVariant: "danger",
    });
  };

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

  setUpItems = (items) => {
    var unpackedItems = items.map((elem, index) => {
      var bufItem = { id: index + 1 };
      Object.entries(elem).forEach(([key, val]) => {
        if (key === "Date") {
          bufItem.date = val;
        } else if (key.includes("USD") && key.includes("rate")) {
          bufItem.usd_rate = val;
        } else if (key.includes("USD") && key.includes("sales")) {
          bufItem.usd_sales = val;
        } else if (key.includes("rate")) {
          bufItem.rate = val;
        } else if (key.includes("sales")) {
          bufItem.sales = val;
        }
      });
      return bufItem;
    });

    return unpackedItems;
  };
}
