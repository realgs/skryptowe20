import React, {Component} from 'react';
import DatePicker from "react-date-picker";
import './SpanCurrencies.css'
import axios from "axios";
import ErrorModelComponent from "../backendModels/ErrorModelComponent";
import CurrencyDataComponent from "../backendModels/CurrencyDataComponent";
import CurrencyDataFunComponent from "../backendModels/CurrencyDataFunComponent";

class SpanCurrenciesComponent extends Component {
    state = {
        dateFrom: new Date(),
        dateTo: new Date(),
        isError: false,
        errorMessage: null,
        errorCode: null,
        isDataPresent: false,
        dataValue: [],
    }

    setMaxDate = () => {
        return this.state.dateTo == null ? new Date() : this.state.dateTo;
    }
    onChangeStartDate = (date) => {
        this.setState({dateFrom: date});
    }
    onChangeEndDate = (date) => {
        this.setState({dateTo: date});
    }
    getValidDateInputAsString = (date) => {
        const day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate();
        const month = date.getMonth() < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1;
        const year = date.getFullYear();
        return year + '-' + month + '-' + day;
    }
    onClick = () => {
        const {dateFrom, dateTo} = this.state;
        const startDate = this.getValidDateInputAsString(dateFrom);
        const endDate = this.getValidDateInputAsString(dateTo);

        this.setState({ isError: false, isDataPresent: false });
        console.log(startDate);
        console.log(endDate);
        axios.get('http://localhost:5000/api/rates/fordatespan?from=' + startDate + '&to=' + endDate)
            .then(res => {
                    this.setState({
                        isDataPresent: true,
                        dataValue: res.data
                    });
            },
                error => {
                    this.setState({
                        isError: true,
                        errorMessage: error.response.data,
                        errorCode: error.response.status
                    });
                });
    }
    renderError = () => {
        return (
            <div>
                {this.state.isError &&
                <ErrorModelComponent
                    errorCode={this.state.errorCode}
                    errorMessage={this.state.errorMessage}
                />}
            </div>
        );
    }
    renderData = () => {
        return (
            <div>
                {this.state.isDataPresent &&
                <CurrencyDataFunComponent
                    data={this.state.dataValue}
                />}
            </div>
        );
    }


    render() {
        return (
            <main className="container">
                <form>
                    <span>
                        <b>
                            Please specify date in format: MM/DD/YYYY
                        </b>
                        <br/>
                    </span>
                    <label htmlFor="datePicker">Starting date</label>
                    <DatePicker
                        id="datePicker"
                        value={this.state.dateFrom}
                        onChange={e => this.onChangeStartDate(e)}
                        maxDate={this.setMaxDate()}
                    />
                    <label htmlFor="datePicker2">Ending date</label>
                    <DatePicker
                        id="datePicker2"
                        value={this.state.dateTo}
                        onChange={e => this.onChangeEndDate(e)}
                        maxDate={new Date()}
                        minDate={this.state.dateFrom}
                    />
                    <button
                        type="button"
                        className="btn btn-primary m-3"
                        onClick={this.onClick}
                    >
                        Submit
                    </button>
                    {this.renderError()}
                    {this.renderData()}
                </form>
            </main>
        );
    }
}

export default SpanCurrenciesComponent;
