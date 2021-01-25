import React, {useState} from 'react';
import DatePicker from 'react-datepicker';
import {Container, Col, Row} from 'react-bootstrap';
import {getRates} from '../api';
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Legend, Tooltip} from 'recharts';

import "react-datepicker/dist/react-datepicker.css";
import { Button } from '@material-ui/core';

function parseResponse(data, code) {
    console.log(typeof []);
    console.log(typeof data);
    if (code === 200 && Array.isArray(data)){
        var res = '[';
        data.forEach((obj) => res += `{ 'date': ${obj.date}, 'rate': ${obj.rate}, 'interpolated': ${obj.interpolated} }, `);
        if (data.length != 0)
        {
            res = res.slice(0, -2);
        }
        return res + ']';
    }
    else return data;
}

export default function Rates() 
{
    const [dateFrom, setDateFrom] = useState(new Date());
    const [dateTo, setDateTo] = useState(new Date());
    const [textAreaValue, setTextAreaValue] = useState([]);
    const [errorCode, setErrorCode] = useState();
    const [chartHidden, setChartHidden] = useState(true);
    
    return (
        <Container fluid style={{textAlign: 'left'}}>
            <Row>
                <Col xs={3}>
                    <h1>Rates</h1>
                    <h4>Date from</h4>
                    <DatePicker selected={dateFrom} onChange={date => {console.log(date); setDateFrom(date);}} />
                    <h4>Date to</h4>
                    <DatePicker selected={dateTo} onChange={date => {console.log(date); setDateTo(date)}} />
                    <Row style={{marginLeft: '0px', marginTop: '20px'}}>
                        <Button variant='contained' color='primary' onClick={() => {
                            console.log('button:');
                            console.log(dateFrom);
                            console.log(dateTo);
                            getRates(dateFrom, dateTo)
                                .then(res => {
                                    setErrorCode(res.status)
                                    if (res.status == '200') {
                                        setTextAreaValue(res.data);
                                        if (res.data.length > 1)
                                        {
                                            setChartHidden(false);
                                        }
                                        else
                                        {
                                            setChartHidden(true);
                                        }
                                    }
                                    else {
                                        setTextAreaValue(res.status + res.data);
                                        setChartHidden(true);
                                    }
                                })
                                .catch(err => {setErrorCode(500); setTextAreaValue(err); setChartHidden(true);})
                        }}>Try it out</Button>
                    </Row>
                </Col>
                <Col>
                    <Row>
                        <h3>JSON response:</h3><br/>
                    </Row>
                    <Row>
                        <textarea value={parseResponse(textAreaValue, errorCode)} style={{width: '1050px', height:'200px', resize: 'none'}} readOnly/>
                    </Row>
                    <Row hidden={chartHidden}>
                        <h3>Diagram:</h3><br/>
                    </Row>
                    <Row hidden={chartHidden}>
                        <LineChart width={1000} height={400} data={textAreaValue} style={{}}>
                            <XAxis dataKey="date" name="Date"/>
                            <YAxis domain={['dataMin - 0.3', 'dataMax + 0.4']}/>
                            <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
                            <Tooltip/>
                            <Legend verticalAlign="top" height={36}/>
                            <Line type="linear" dot={false} dataKey="rate" stroke="#27165c" name="USD to PLN"/>
                        </LineChart>
                    </Row>
                </Col>
            </Row>
        </Container>
    )
}
