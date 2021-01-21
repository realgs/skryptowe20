import React, { Component } from "react";
import "./App.css";
import { BrowserRouter as Router, Route } from "react-router-dom";
import { Navbar, Nav, Form } from "react-bootstrap";
import About from "./components/about";
import Exchanges from "./components/exchanges";
import Sales from "./components/sales";

export default class App extends Component {
  state = {
    currencies: ["USD", "EUR", "HUF", "CHF", "GBP", "JPY", "CZK", "AED", "BOB"],
    github: "https://github.com/wasyl078/skryptowe20/tree/L5",
    nbp: "http://api.nbp.pl",
    linkedIn: "https://www.linkedin.com/in/maciej-wasilewski-a956b71a3/",
    bootstrapUrl: "getbootstrap.com",
    sales: "https://data.world/state-of-connecticut/5mzw-sjtu",
  };

  render() {
    return (
      <Router>
        <div className="container">
          <div className="my-nav-bar m-1">
            <Navbar bg="dark" variant="dark fixed-top ">
              <div className="container">
                <Navbar.Brand>NBP API by Maciej Wasilewski</Navbar.Brand>
                <Nav className="mr-auto ">
                  <Nav.Link href="/">About</Nav.Link>
                  <Nav.Link href="/exchanges">Exchanges</Nav.Link>
                  <Nav.Link href="/sales">Sales</Nav.Link>
                </Nav>
                <Form inline></Form>
              </div>
            </Navbar>
          </div>
          <Route
            exact
            path="/"
            render={() => (
              <About
                github={this.state.github}
                currencies={this.state.currencies}
                sales={this.state.sales}
              />
            )}
          />
          <Route
            path="/exchanges"
            render={() => (
              <Exchanges
                github={this.state.github}
                currencies={this.state.currencies}
                sales={this.state.sales}
              />
            )}
          />
          <Route
            path="/sales"
            render={() => (
              <Sales
                github={this.state.github}
                currencies={this.state.currencies}
              />
            )}
          />
        </div>
      </Router>
    );
  }
}
