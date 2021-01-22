import {Route, BrowserRouter as Router, Switch} from 'react-router-dom';
import Income from './pages/Income';
import ApiInfo from './pages/ApiInfo';
import Rates from './pages/Rates';
import Error from './pages/Error';
import {Navbar, Nav} from 'react-bootstrap';
import './App.css';

function App() {
  return (
    <div className="App">
      <Navbar bg="dark" expand="lg">
        <Navbar.Brand href="/" style={{color: 'white'}}>Currency api</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link href="rates" style={{color: 'white'}}>Rates</Nav.Link>
            <Nav.Link href="income" style={{color: 'white'}}>Income</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
      <div className='container-fill' style={{height: '100%'}}>
        <Router>
          <Switch>
          <Route path='/' exact component={ApiInfo} />
          <Route path='/rates' component={Rates} />
          <Route path='/income' component={Income} />
          <Route path='/' component={Error} />
          </Switch>
        </Router> 
      </div>
    </div>
  );
}

export default App;
