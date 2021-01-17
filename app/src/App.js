import React, { useState, useEffect } from "react";
import "./App.css";
import MyNavBar from "./components/myNavBar";
import CardInfo from "./components/cardInfo";
import CardTable from "./components/cardTable";

function App() {
  return (
    <div className="body">
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
    </div>
  );
}

export default App;
