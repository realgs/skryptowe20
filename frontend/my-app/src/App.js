import './App.css';
import DataTable from './DataTable'
import Home from './Home'
import React from 'react';
import {Route, Link} from 'react-router-dom';

function App() {
    return (
        <div className="App">
            <header Access-Control-Allow-Origin="*" />
		    <Route exact path="/" component={Home}/>
		    <Route exact path="/result" component={DataTable}/>
        </div>
    );
}

export default App;
