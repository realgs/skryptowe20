import React, {Component} from 'react'
import ErrorModelComponent from "../backendModels/ErrorModelComponent";
import SalesDataFunComponent from "../backendModels/SalesDataFunComponent";
import axios from "axios";
import DatePicker from "react-date-picker";


class SalesComponent extends Component {
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
                <SalesDataFunComponent data={this.state.dataValue}/>
                }
            </div>
        )
    }
    onChange = (date) => {
        this.setState({date});
    }
    createObject(date, pln, usd) {
        return {date, pln, usd};
    }
    onClick = () => {
        const {date} = this.state;
        this.setState({isError: false, isDataPresent: false});

        if (date != null) {
            const day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate();
            const month = date.getMonth() < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1;
            const year = date.getFullYear();
            const dataString = year + '-' + month + '-' + day;

            axios.get('http://localhost:5000/api/sales/fordate?date=' + dataString)
                .then(res => {
                        var valu = [];
                        valu.push(this.createObject(res.data['date'], res.data['plnSalesValue'], res.data['usdSalesValue']));
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

export default SalesComponent;
