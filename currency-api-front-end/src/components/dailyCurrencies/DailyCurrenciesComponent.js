import React, {Component} from 'react';
import DatePicker from "react-date-picker";
import axios from "axios";
import ErrorModelComponent from "../backendModels/ErrorModelComponent";
import DailyCurrencyDataComponent from "../backendModels/DailyCurrencyDataComponent";

class DailyCurrenciesComponent extends Component {
    state = {
        date: new Date(),
        isError: false,
        errorMessage: null,
        errorCode: null,
        isDataPresent: false,
        dataValue: null,
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
        const {dataValue} = this.state;
        return (
            <div>
                {this.state.isDataPresent &&
                <DailyCurrencyDataComponent
                    date={dataValue['date']}
                    interpolation={dataValue['interpolation']}
                    price={dataValue['price']}
                />}
            </div>
        )
    }

    onChange = (date) => {
        // console.log('ONCHANGEVALUE', event)
        this.setState({date});
    }

    onClick = (event) => {
        const {date} = this.state;
        const day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate();
        const month = date.getMonth() < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1;
        const year = date.getFullYear();
        
        const dataString = year + '-' + month + '-' + day;
        this.setState({isError: false, isDataPresent: false});
        console.log(dataString);
        axios.get('http://localhost:5000/api/rates/fordate?date=' + dataString)
            .then(res => {
                    this.setState({
                        isDataPresent: true,
                        dataValue: res.data
                    });
                    console.log(this.state.isDataPresent);
                    console.log(this.state.dataValue['date']);
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
                        id="datePicker"
                        value={this.state.date}
                        onChange={e => this.onChange(e)}
                        maxDate={new Date()}/>
                    <button
                        type="button"
                        className="btn btn-primary m-3"
                        onClick={e => this.onClick(e)}
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
