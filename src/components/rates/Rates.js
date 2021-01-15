import React, { useState } from 'react'
import {Container,Row,Col} from 'react-bootstrap'
import {Tabs,Tab} from 'react-bootstrap'
import DatePicker from 'react-datepicker'
import "react-datepicker/dist/react-datepicker.css";
import '../Styles.css'
import axios from 'axios'
import RatesResults from './RatesResults'

function Rates() {
    return (
        <div>
            <Container>
                <Row>
                <Col xs={12}><RatesContext /></Col>
                </Row>
            </Container>
        </div>
    )
}

function RatesContext() {
    const [resultApi, setResult] = useState([])
    const catchResult = (result) => setResult(result)
    const clearTable = () => setResult([])
    return (
        <div>
            <br/>
            <Tabs fill defaultActiveKey="oneDay" id="uncontrolled-tab-example" onSelect={clearTable}>
                <Tab eventKey="oneDay" title="Konkretny dzień">
                    <RatesCurrencyChooser />
                    <RatesForm zlapWynik={catchResult}/>
                    <br/>
                    <RatesResults resultApi={resultApi}/>
                </Tab>
                <Tab eventKey="multiDays" title="Przedział dni">
                    <RatesCurrencyChooser />
                    <RatesFormMulti zlapWynik={catchResult}/>
                    <br/>
                    <RatesResults resultApi={resultApi}/>
                </Tab>
            </Tabs>
        </div>
    )
}

function RatesCurrencyChooser() {
    return (
        <Tabs fill defaultActiveKey="usd" id="uncontrolled-tab-example">
            <Tab eventKey="usd" title="USD">
                {/* Todo: Setting the currency to different if implemented */}
            </Tab>
            <Tab eventKey="eur" title="EUR" disabled>
                <h1>Err</h1>
            </Tab>
            <Tab eventKey="yin" title="YIN" disabled>
                <h1>Err</h1>
            </Tab>
        </Tabs>
    )
}

function RatesForm(props) {
    const {zlapWynik} = props
    const [startDate, setStartDate] = useState(new Date(2007, 1, [16]))
    const datePick = async (date) => {
        try {
            const result = await axios.get(`https://rates-and-sales-api.herokuapp.com/api/rates/USD/${formatDate(date)}`)
            zlapWynik(result.data.rates ? result.data.rates : [])
        } catch(error) {
            zlapWynik([error.response.data])
        }
    }
    return (
        <div>
            <br/>
            <p class='datePick'> Wybierz datę: {' '}
                <DatePicker 
                    selected={startDate} 
                    onSelect={date => datePick(date)}
                    onChange={date => setStartDate(date)} 
                /> 
            </p>
        </div>
    )
}

function RatesFormMulti(props) {
    const {zlapWynik} = props
    const [startDate, setStartDate] = useState(new Date(2007, 1, [16]))
    const [endDate, setEndDate] = useState(new Date(2007, 1, [18]))
    const datePick = async (startDate, endDate) => {
        try {
            const result = await axios(`https://rates-and-sales-api.herokuapp.com/api/rates/USD/${formatDate(startDate)}/${formatDate(endDate)}`)
            zlapWynik(result.data.rates ? result.data.rates : [])
        } catch(error) {
            zlapWynik([error.response.data])
        }
    }
    return (
        <div>
            <br/>
            <p className='datePick'> Wybierz datę początkową: {' '}
                <DatePicker 
                    selected={startDate} 
                    onSelect={date => datePick(date, endDate)}
                    onChange={date => setStartDate(date)} 
                /> {' '}
                <br/><br/>
                Wybierz datę końcową: {' '}
                <DatePicker 
                    selected={endDate} 
                    onSelect={date => datePick(startDate, date)}
                    onChange={date => setEndDate(date)} 
                /> {' '}
            </p>
        </div>
    )
}

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

    return [year, month, day].join('-');
}

export default Rates
