import React from 'react';
import {Navbar,Nav} from 'react-bootstrap';
import Home from './Home';
import Rates from './rates/Rates';
import Sales from './sales/Sales';
import {
    BrowserRouter as Router,
    Switch,
    Route
} from "react-router-dom";

function SimpleNavbar() {
  return (
    <Router>
    <div className="SimpleNavbar">
        <Navbar bg="dark" variant="dark">
            <Navbar.Brand href="/">Rates and Sales API</Navbar.Brand>
            <Nav className="mr-auto">
            <Nav.Link href="/">Home</Nav.Link>
            <Nav.Link href="/rates">Rates</Nav.Link>
            <Nav.Link href="/sales">Sales</Nav.Link>
            </Nav>
        </Navbar>
        <Switch>
          <Route path="/sales">
            <Sales />
          </Route>
          <Route path="/rates">
            <Rates />
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
    </div>
    </Router>
  );
}

export default SimpleNavbar;