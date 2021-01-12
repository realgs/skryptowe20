import React, {Component} from 'react';
import DatePicker from "react-date-picker";
import axios from "axios";
import ErrorModelComponent from "../backendModels/ErrorModelComponent";
import CurrencyDataComponent from "../backendModels/CurrencyDataComponent";
import CurrencyDataFunComponent from "../backendModels/CurrencyDataFunComponent";
import CustomPaginationTable from "../backendModels/CurrencyDataFunComponent";

class DailyCurrenciesComponent extends Component {
    state = {
        date: new Date(),
        isError: false,
        errorMessage: null,
        errorCode: null,
        isDataPresent: false,
        dataValue: [],
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
                    <CustomPaginationTable data={this.state.dataValue}/>
                /*<CurrencyDataFunComponent
                    data={this.state.dataValue}
                />*/
                }
            </div>
        )
    }

    onChange = (date) => {
        this.setState({date});
    }
    createObject(date, price, interpolation) {
        const interpolationValue = interpolation ? 'true' : 'false';
        return {date, price, interpolationValue};
    }
    onClick = () => {
        const {date} = this.state;
        const day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate();
        const month = date.getMonth() < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1;
        const year = date.getFullYear();

        const dataString = year + '-' + month + '-' + day;
        this.setState({isError: false, isDataPresent: false});
        axios.get('http://localhost:5000/api/rates/fordate?date=' + dataString)
            .then(res => {
                    var valu = [];
                    valu.push(this.createObject(res.data['date'], res.data['price'], res.data['interpolation']));
                    this.setState({
                        isDataPresent: true,
                        dataValue: valu
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


    render() {
        return (
            <main className="container">
                <form>
                    <span><b>Please specify date in format: MM/DD/YYYY </b><br/></span>
                    <DatePicker
                        value={this.state.date}
                        onChange={e => this.onChange(e)}
                        maxDate={new Date()}/>
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

export default DailyCurrenciesComponent;
