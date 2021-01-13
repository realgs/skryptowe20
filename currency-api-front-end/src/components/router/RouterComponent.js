import React, {Component} from 'react';
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import HomeComponent from "../home/HomeComponent";
import DailyCurrenciesComponent from "../dailyCurrencies/DailyCurrenciesComponent";
import DailySalesComponent from "../dailySales/DailySalesComponent";
import SpanCurrenciesComponent from "../spanCurrencies/SpanCurrenciesComponent";
import NavBarComponent from "../navbar/NavBarComponent";
import SpanSalesComponent from "../spanSales/SpanSalesComponent";


class RouterComponent extends Component {
    render() {
        return (
            <Router>
                <NavBarComponent/>
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
                    <Route path="/dailySales">
                        <DailySalesComponent/>
                    </Route>
                    <Route path="/spanSales">
                        <SpanSalesComponent/>
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
