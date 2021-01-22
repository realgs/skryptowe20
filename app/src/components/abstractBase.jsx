import React, { Component } from "react";
import Badge from "react-bootstrap/Badge";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";

export default class AbstractBase extends Component {
  state = {
    chosenCurrency: "Choose Currency",
    chosenOption: false,
    resultBadgeVariant: "danger",
    resultBadgeText: "No results yet",
    chosenBeginningDate: null,
    chosenEndingDate: null,
    items: null,
    chartReady: false,
    tableReady: false,
    actualChart: null,
  };

  // Universal components
  infoBadge = (text, variant) => {
    return (
      <h2>
        <Badge className="mx-2 mt-2" variant={variant}>
          {text}
        </Badge>
      </h2>
    );
  };

  dropdownCurrencies = (currencies) => {
    return (
      <DropdownButton
        className="format m-2"
        id="dropdown-item-button"
        title={this.state.chosenCurrency}
      >
        {currencies.map((elem, index) => (
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
            onChange={(value) => this.updateChosenBeginningDate(value)}
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

  footer = () => {
    return (
      <div className="card-footer border-primary text-muted">
        More info at my <a href={this.props.github}>github page</a>
      </div>
    );
  };

  // Utils
  updateChosenCurrency = (value) => {
    this.setState({ chosenCurrency: value });
  };

  updateChosenBeginningDate = (value) => {
    this.setState({ chosenBeginningDate: this.formatDate(value) });
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

  checkParams = () => {
    var errorOccured = false;
    if(this.state.chosenCurrency.includes("Choose Currency")){
        this.setState({
          resultBadgeText: "Choose Currency!!!",
          resultBadgeVariant: "danger",
        });
        errorOccured = true;
      }
      else if(this.state.chosenBeginningDate === null || this.state.chosenEndingDate === null){
        this.setState({
          resultBadgeText: "Choose Proper Date!",
          resultBadgeVariant: "danger",
        });
        errorOccured = true;
      }
    return errorOccured;
  }
}
