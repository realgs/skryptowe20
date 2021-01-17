import React, { Component } from "react";

export default class MyNavBar extends Component {
  render() {
    return (
      <body className="my-nav-bar">
        <nav className="navbar navbar-dark bg-dark fixed-top">
          <div className="container">
            <text className="navbar-brand">NBP API by Maciej Wasilewski</text>
          </div>
        </nav>
      </body>
    );
  }
}
