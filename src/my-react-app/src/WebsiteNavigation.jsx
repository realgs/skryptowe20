import React, { Component } from "react";
import { Link } from "react-router-dom";
import { Nav, Navbar } from "react-bootstrap";

class WebsiteNavigation extends Component {
  state = {};
  render() {
    return (
      <Navbar collapseOnSelect expand="lg" className="navbar-dark bg-primary" >
        <Link to="/" className="navbar-brand">
          <img src="dolar.svg" width="30" height="30" alt=""></img>
        </Link>
        <Navbar.Toggle />
        <Navbar.Collapse>
          <Nav className="mr-auto">
            <Nav.Item>
              <Link to="/" className="nav-link">
                About
              </Link>
            </Nav.Item>
            <Nav.Item>
              <Link to="/form/chart" className="nav-link">
                Charts
              </Link>
            </Nav.Item>
            <Nav.Item>
              <Link to="/form/table" className="nav-link">
                Table
              </Link>
            </Nav.Item>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    );
  }
}

export default WebsiteNavigation;
