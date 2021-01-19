import React, { Component } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import WebsiteNavigation from "./WebsiteNavigation";
import AboutTab from "./AboutTab";
import ChartTab from "./ChartTab";
import TableTab from "./TableTab";
import InfoModal from "./Common/InfoModal";

class App extends Component {
  state = {
    showModal: false,
    label: "",
    labels: [],
    data: [],
    modalTitle: "",
    modalText: "",
  };

  editModal = (show, title, text) => {
    this.setState({
      showModal: show,
      modalTitle: title,
      modalText: text,
    });
  };

  closeModal = () => {
    this.editModal(false, "", "");
  };

  handleBadInput = () => {
    this.editModal(
      true,
      "Not enought parameter",
      "You forgot to fill all form inputs, try again!"
    );
  };

  handleBadRequest = () => {
    this.editModal(
      true,
      "Wrong parameters",
      "You probably picked an unsupported currency, try again!"
    );
  };

  handleNoData = () => {
    this.editModal(
      true,
      "No data to display",
      "No data in given time period, try with a different one!"
    );
  };

  handleWrongDateOrder = () => {
    this.editModal(
      true,
      "Wrong date order",
      "Your dates are in the wrong order, fix it and try again!"
    );
  };

  validateDates = (from, to) => {
    const fromParsed = new Date(from);
    const toParsed = new Date(to);
    return fromParsed <= toParsed;
  };

  fetchApi = async (route, currency, from, to) => {
    if (this.validateDates(from, to)) {
      const response = await fetch(`/${route}/${currency}/time/${from}/${to}`);
      if (response.status === 200) {
        const json = await response.json();
        if (json.length > 0) {
          return json;
        } else {
          this.handleNoData();
        }
      } else {
        this.handleBadRequest();
      }
    } else {
      this.handleWrongDateOrder();
    }
  };

  fetchCurrency = async (currency, from, to) => {
    const result = await this.fetchApi("currency", currency, from, to);
    if (result !== undefined) {
      const labels = result.map((e) => e.date);
      const data = result.map((e) => e.exchange_rate);
      console.log(labels, data);
      this.setState({ labels, data, label: "Exchange rates" });
    }
  };

  fetchSales = async (currency, from, to) => {
    const result = await this.fetchApi("sales", currency, from, to);
    if (result !== undefined) {
      console.log(result);
      const labels = result.map((e) => e.date);
      const data = result.map((e) => e.requested);
      this.setState({ labels, data, label: "Sales" });
    }
  };

  render() {
    return (
      <Router>
        <WebsiteNavigation />
        <main className="container pt-3">
          <InfoModal
            show={this.state.showModal}
            closeModal={this.closeModal}
            title={this.state.modalTitle}
            text={this.state.modalText}
          />
          <Switch>
            <Route path="/" exact component={() => <AboutTab />} />
            <Route
              path="/table"
              component={() => (
                <TableTab
                  labels={this.state.labels}
                  data={this.state.data}
                  fetchCurrency={this.fetchCurrency}
                  fetchSales={this.fetchSales}
                  label={this.state.label}
                />
              )}
            />
            <Route
              path="/chart"
              component={() => (
                <ChartTab
                  labels={this.state.labels}
                  data={this.state.data}
                  fetchCurrency={this.fetchCurrency}
                  fetchSales={this.fetchSales}
                  label={this.state.label}
                />
              )}
            />
          </Switch>
        </main>
      </Router>
    );
  }
}

export default App;
