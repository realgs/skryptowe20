import React, {Component} from 'react';
import {
    BrowserRouter as Router,
    Route,
    Switch
} from "react-router-dom";
import HomeComponent from "../home/HomeComponent";
import DailyCurrenciesComponent from "../dailyCurrencies/DailyCurrenciesComponent";
import SalesComponent from "../sales/DailySalesComponent";
import SpanCurrenciesComponent from "../spanCurrencies/SpanCurrenciesComponent";
import NavBarComponent from "../navbar/NavBarComponent";

class RouterComponent extends Component {
    render() {
        return (
            <Router>
                <NavBarComponent />
                <Switch>
                    <Route exact path="/">
                        <HomeComponent/>
                    </Route>
                    <Route path="/dailyCurrencies">
                        <DailyCurrenciesComponent/>
                    </Route>
                    <Route path="/spanCurrencies">>
                        <SpanCurrenciesComponent/>
                    </Route>
                    <Route path="/sales">>
                        <SalesComponent/>
                    </Route>
                    <Route path="*">
                        <HomeComponent/>
                    </Route>
                </Switch>
            </Router>
        );
    }
}

export default RouterComponent;
