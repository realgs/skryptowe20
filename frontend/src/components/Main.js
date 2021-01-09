import { Switch, Route } from 'react-router-dom'
import * as React from "react";
import Home from "./Home";
import Sales from "./Sales";
import Currency from "./Currency";

const Main = () => {
    return(
        <main>
            <Switch>
                <Route exact path='/' component={Home}/>
                <Route path='/sales' component={Sales}/>
                <Route path='/currency' component={Currency}/>
            </Switch>
        </main>
    );
}

export default Main
