import './App.css';
import ExchangeRates from "./components/ExchangeRates";

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
                    <a className="nav-link active" id="home-tab" data-bs-toggle="tab" href="#home" role="tab"
                       aria-controls="home" aria-selected="true">Exchange rates</a>
                </li>
                <li className="nav-item" role="presentation">
                    <a className="nav-link" id="profile-tab" data-bs-toggle="tab" href="#profile" role="tab"
                       aria-controls="profile" aria-selected="false">Sales Information</a>
                </li>
                <li className="nav-item" role="presentation">
                    <a className="nav-link" id="contact-tab" data-bs-toggle="tab" href="#contact" role="tab"
                       aria-controls="contact" aria-selected="false">Contact</a>
                </li>
            </ul>
            <div className="tab-content" id="myTabContent">
                <div className="tab-pane fade show active" id="home" role="tabpanel" aria-labelledby="home-tab">
                    <ExchangeRates/>
                </div>
                <div className="tab-pane fade" id="profile" role="tabpanel" aria-labelledby="profile-tab">...</div>
                <div className="tab-pane fade" id="contact" role="tabpanel" aria-labelledby="contact-tab">...</div>
            </div>
        </div>
    );
}

export default App;
