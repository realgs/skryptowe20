import React, { Component } from "react";

export default class MyNavBar extends Component {
  render() {
    return (
      <div className="my-nav-bar">
        <nav className="navbar navbar-dark bg-dark fixed-top">
          <div className="container">
            <div className="navbar-brand">NBP API by Maciej Wasilewski</div>
          </div>
        </nav>
      </div>
    );
  }
}
