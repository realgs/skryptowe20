import Button from "react-bootstrap/Button";
import Table from "react-bootstrap/Table";
import Chart from "chart.js";
import AbstractBase from "./abstractBase";
import "react-calendar/dist/Calendar.css";

export default class Exchanges extends AbstractBase {
  constructor(props) {
    super(props);
    this.state = {
      ...this.state,
      interpolation: false,
      interpolationResultsPresent: false,
    };
  }

  callApi = () => {
    if(this.checkParams()){
      return
    }
    const interAddon = this.state.interpolation ? "/inter/" : "/";
    fetch(
      "/rates" +
        interAddon +
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

  createChart = () => {
    if (this.state.items != null && !this.state.chosenOption) {
      var labels = [];
      var dataset = [];
      this.state.items.forEach((x) => {
        dataset.push(x.rate);
        labels.push(x.date);
      });
      if (this.state.actualChart !== null) {
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
    this.setState({ actualChart: chart });
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
    this.setState({ actualChart: chart });
  };

  render() {
    return (
      <div className="container">
        <div className="card border-primary mb-5">
          <div className="card-header border-primary">
            <div>{this.infoBadge("You Are Now At Exchange Rates Page", "primary")}</div>
          </div>
          <div className="card-body">
            <div className="d-flex">
              <div>{this.dropdownCurrencies(this.props.currencies)}</div>
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
  updateInterpolation(event) {
    this.setState({ interpolation: !this.state.interpolation });
  }
}
