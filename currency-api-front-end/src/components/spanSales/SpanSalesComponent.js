import React, {Component} from 'react'
import ErrorModelComponent from "../backendModels/ErrorModelComponent";
import SalesDataFunComponent from "../backendModels/SalesDataFunComponent";
import axios from "axios";
import DatePicker from "react-date-picker";
import {Line, LineChart, XAxis, YAxis} from "recharts";


class SpanSalesComponent extends Component {
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
        this.setState({isError: false, isDataPresent: false});

        if (dateFrom != null && dateTo != null) {
            const startDate = this.getValidDateInputAsString(dateFrom);
            const endDate = this.getValidDateInputAsString(dateTo);

            axios.get('http://localhost:5000/api/sales/fordatespan?from=' + startDate + '&to=' + endDate)
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
        } else {
            this.setState({
                isError: true,
                errorMessage: 'Date cannot be null',
                errorCode: -1
            })
        }
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
                <React.Fragment>
                    <SalesDataFunComponent
                        data={this.state.dataValue}
                    />
                    <div style={{height: 400, width: 400}}>
                        <LineChart
                            width={400}
                            height={400}
                            data={this.state.dataValue}
                            margin={{
                                top: 5,
                                right: 20,
                                bottom: 5,
                                left: 0
                            }}
                        >
                            <Line
                                type="monotone"
                                dataKey="usdSalesValue"
                                stroke="#8884d8"
                                dot={false}
                            />
                            <XAxis dataKey="date"/>
                            <YAxis/>
                        </LineChart>
                    </div>
                </React.Fragment>}
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

export default SpanSalesComponent;
