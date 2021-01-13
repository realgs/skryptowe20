import React, {Component} from 'react';
import DatePicker from "react-date-picker";
import axios from "axios";
import ErrorModelComponent from "../backendModels/ErrorModelComponent";
import CurrencyDataFunComponent from "../backendModels/CurrencyDataFunComponent";

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
                <CurrencyDataFunComponent data={this.state.dataValue}/>
                }
            </div>
        )
    }
    onChange = (date) => {
        this.setState({date});
    }
    onClick = () => {
        const {date} = this.state;
        this.setState({isError: false, isDataPresent: false});

        if (date != null) {
            const day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate();
            const month = date.getMonth() < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1;
            const year = date.getFullYear();
            const dataString = year + '-' + month + '-' + day;

            axios.get('http://localhost:5000/api/rates/fordate?date=' + dataString)
                .then(res => {
                        this.setState({
                            isDataPresent: true,
                            dataValue: [{
                                date: res.data['date'],
                                price: res.data['price'],
                                interpolation: res.data['interpolation'] ? 'true' : false
                            }]
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
            });
        }
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
