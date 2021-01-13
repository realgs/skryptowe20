import React, {Component} from "react";
import {Link} from "react-router-dom";
import './NavBar.css'


class NavBarComponent extends Component {
    render() {
        return (
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
                <div className="container-fluid">
                    <a className="navbar-brand" href="/">CurrencyAPI</a>
                    <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
                        <div className="navbar-nav">
                            <Link to='/' className="myLink">Home </Link>
                            <Link to="/dailyCurrencies" className="myLink">DailyCurrencies</Link>
                            <Link to="/spanCurrencies" className="myLink">SpanCurrencies</Link>
                            <Link to="/dailySales" className="myLink">DailySales</Link>
                            <Link to="/spanSales" className="myLink">SpanSales</Link>
                        </div>
                    </div>
                </div>
            </nav>
        );
    }
}

export default NavBarComponent;
