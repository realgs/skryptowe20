import { Switch, Route } from 'react-router-dom'
import * as React from "react";
import Home from "./Home";
import Sales from "./Sales";
import Currency from "./Currency";

const Main = () => {
    return (
        <main>
            <Switch>
                <Route exact path='/'>
                    <Home />
                </Route>
                <Route path='/currency'>
                    <Currency />
                </Route>
                <Route path='/sales'>
                    <Sales />
                </Route>
            </Switch>
        </main>
    );
}

export default Main
