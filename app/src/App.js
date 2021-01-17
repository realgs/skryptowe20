import React, { useState, useEffect } from "react";
import "./App.css";
import MyNavBar from "./components/myNavBar";
import CardInfo from "./components/cardInfo";
import CardTable from "./components/cardTable";

function App() {
  const styles = {
    paddingTop: "20px",
  };

  return (
    <body className="body">
      <MyNavBar />
      <div className="container">
        <div className="row">
          <div className="column">
            <CardInfo />
          </div>
        </div>
        <div className="row">
          <div className="column">
            <CardTable />
          </div>
        </div>
      </div>
    </body>
  );
}

export default App;
