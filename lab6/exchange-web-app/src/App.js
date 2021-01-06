import './App.css';
import ExchangeRates from "./components/ExchangeRates";
import SalesInformation from "./components/SalesInformation";
import ApiDocs from "./components/ApiDocs";

function App() {
    return (
        <div className="App">
            <nav className="navbar navbar-dark bg-dark">
                <div className="container-fluid">
                    <a className="navbar-brand" href="#">
                        <h4 className="text-white">Exchange App</h4>
                    </a>
                </div>
            </nav>
            <ul className="nav nav-tabs" id="myTab" role="tablist">
                <li className="nav-item" role="presentation">
                    <a className="nav-link active" id="exchange-rates-tab" data-bs-toggle="tab" href="#exchange-rates"
                       role="tab"
                       aria-controls="home" aria-selected="true">Exchange rates</a>
                </li>
                <li className="nav-item" role="presentation">
                    <a className="nav-link" id="sales-info-tab" data-bs-toggle="tab" href="#sales-info" role="tab"
                       aria-controls="profile" aria-selected="false">Sales Information</a>
                </li>
                <li className="nav-item" role="presentation">
                    <a className="nav-link" id="api-docs-tab" data-bs-toggle="tab" href="#api-docs" role="tab"
                       aria-controls="profile" aria-selected="false">Api Docs</a>
                </li>
            </ul>
            <div className="tab-content" id="myTabContent">
                <div className="tab-pane fade show active" id="exchange-rates" role="tabpanel"
                     aria-labelledby="exchange-rates-tab">
                    <ExchangeRates/>
                </div>
                <div className="tab-pane fade" id="sales-info" role="tabpanel" aria-labelledby="sales-info-tab">
                    <SalesInformation/>
                </div>
                <div className="tab-pane fade" id="api-docs" role="tabpanel" aria-labelledby="api-docs-tab">
                    <ApiDocs/>
                </div>
            </div>
        </div>
    );
}

export default App;
