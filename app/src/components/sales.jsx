import React from "react";
import Table from "react-bootstrap/Table";
import Chart from "chart.js";
import AbstractBase from "./abstractBase";
import "react-calendar/dist/Calendar.css";

export default class Sales extends AbstractBase {
  componentDidMount() {
    var idx = this.props.currencies.findIndex((e) => {
      return e === "USD";
    });
    var currenciesRemastered = [...this.props.currencies];
    currenciesRemastered[idx] = "PLN";
    this.setState({ currencies: currenciesRemastered });
  }

  constructor(props) {
    super(props);
    this.state = {
      ...this.state,
      currencies: [],
    };
  }

  callApi = () => {
    if(this.checkParams()){
      return
    }
    fetch(
      "/sales/" +
        this.state.chosenCurrency +
        "/" +
        this.state.chosenBeginningDate +
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
      if (this.state.actualChart !== null) {
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
    this.setState({ actualChart: chart });
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
    this.setState({ actualChart: chart });
  };

  render() {
    return (
      <div className="container">
        <div className="card border-primary mb-5">
          <div className="card-header border-primary">
            <div>{this.infoBadge("You Are Now At Sales Page", "warning")}</div>
          </div>
          <div className="card-body">
            <div className="d-flex">
              <div>{this.dropdownCurrencies(this.state.currencies)}</div>
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
