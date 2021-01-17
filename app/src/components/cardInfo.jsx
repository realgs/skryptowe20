import React, { Component } from "react";
import "./../App.css";

class CardInfo extends Component {
  state = {
    currencies: [
      "USD",
      "EUR",
      "HUF",
      "CHF",
      "GBP",
      "JPY",
      "CZK",
      "AED",
      "BOB",
      "KWD",
    ],
  };

  getCurrencies = () => {
    return this.state.currencies.join(", ");
  };

  boldIt = (text) => {
    return <span style={{ fontWeight: "bold" }}>{text}</span>;
  };

  mainTitle = () => {
    return (
      <h2 className="card-title">
        What is
        <span style={{ color: "#2E3F7F", fontStyle: "italic" }}>
          {" "}
          NBP Api by Maciej Wasilewski
        </span>
        ?
      </h2>
    );
  };

  mainGoal = () => {
    return (
      <div>
        Main goal of this project is to create a very reliable and precise API
        for PLN exchange rates and real estate data from state of Connecticut.
        Every user with connection to this API is able to request rates from
        given period and also data about sales in USD and any other actually
        available currency. <br />
        <br />
        <ol>
          <li>
            Clone repo from my{" "}
            <a href="https://github.com/wasyl078/skryptowe20/tree/L5">
              github page
            </a>{" "}
            to your hard drive. <br />
          </li>
          <li>
            {" "}
            Go to{" "}
            <a href="https://data.world/state-of-connecticut/5mzw-sjtu">
              this link
            </a>{" "}
            and download the .csv file. Save it in the same location as the
            repo.
          </li>
          <li>
            Open windows console and navigate to cloned directory and run
            start.bat. This script will automatically create a new python
            virtual environment and database. It will also activate this new
            venv, set-up a database and run the server.
          </li>
          <li>Do not forget to start {this.boldIt("this")} React server</li>
        </ol>
      </div>
    );
  };

  howToUseRates = () => {
    return (
      <div>
        <h4>Exchange Rates API</h4>
        Actually available currencies: {this.getCurrencies()}. These are also
        codes that you are supposed to put as {this.boldIt("code")} argument.
        Arguments marked as {this.boldIt("single_date")} /{" "}
        {this.boldIt("from_date")} / {this.boldIt("till_date")} must be
        formatted as: {this.boldIt("YYYY-MM-DD")} . Data is taken from{" "}
        <a href="http://api.nbp.pl">NBP Api</a>, so you can request data from{" "}
        {this.boldIt("2002-01-02")} till today. <br />
        <br />
        <ul>
          <li>
            Exchange rates from a single day: /rates/inter/{this.boldIt("code")}
            /{this.boldIt("single_date")}{" "}
          </li>
          <li>
            Exchange rates from last X days: /rates/inter/
            {this.boldIt("code")}/{this.boldIt("last_days")}
          </li>
          <li>
            Exchange rates from given date till today: /rates/inter/
            {this.boldIt("code")}/{this.boldIt("from_date")}/today{" "}
          </li>
          <li>
            Exchange rates from given period: /rates/inter/
            {this.boldIt("code")}/{this.boldIt("from_date")} /
            {this.boldIt("till_date")}{" "}
          </li>
          <li>
            You can also request data without "Interpolated flag". Just remove
            /inter from lines presented above.
          </li>
        </ul>
      </div>
    );
  };

  howToUseSales = () => {
    return (
      <div>
        <h4>Sales API</h4>
        Available values for {this.boldIt("code")} are almost the same as for
        exchange rates. The original currency used in the dataset is USD, so you
        cannot request for it, but you can request for data calculated to PLN
        instead. The data comes from Connecicut real estate dataset. Even though
        the file's names says: 2001-2017, the actual data is available only for
        period from 2006-10-01 to 2017-09-29. That's because some parts of
        original .csv file are spoiled. <br />
        <br />
        <ul>
          <li>
            Sales data from single day: /sales/{this.boldIt("code")}/
            {this.boldIt("single_date")}
          </li>
          <li>
            Sales data from given period: /sales/{this.boldIt("code")}/
            {this.boldIt("from_date")}/{this.boldIt("till_date")}
          </li>
        </ul>
      </div>
    );
  };

  divider = () => {
    return <hr />;
  };

  render() {
    return (
      <div className="card mb-5">
        <div className="card-body">
          {this.mainTitle()}
          <p className="card-text">
            {this.mainGoal()}
            {this.divider()}
            {this.howToUseRates()}
            {this.divider()}
            {this.howToUseSales()}
          </p>
        </div>
        <div className="card-footer text-muted">
          More info at my{" "}
          <a href="https://github.com/wasyl078/skryptowe20/tree/L5">
            github page
          </a>
        </div>
      </div>
    );
  }
}

export default CardInfo;
