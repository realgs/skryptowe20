import React, {useState} from 'react';
import DatePicker from 'react-datepicker';
import {Container, Col, Row} from 'react-bootstrap';
import {getIncome} from '../api';
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Legend, Tooltip} from 'recharts';

import "react-datepicker/dist/react-datepicker.css";
import { Button } from '@material-ui/core';

function parseResponse(data, code) {
    console.log(typeof []);
    console.log(typeof data);
    if (code === 200 && Array.isArray(data)){
        var res = '[';
        data.forEach((obj) => res += `{ 'date': ${obj.date}, 'profit_usd': ${obj.profit_usd}, 'profit_pln': ${obj.profit_pln} }, `);
        if (data.length != 0)
        {
            res = res.slice(0, -2);
        }
        return res + ']';
    }
    else return data;
}

export default function Income() 
{
    const [dateFrom, setDateFrom] = useState(new Date());
    const [dateTo, setDateTo] = useState(new Date());
    const [textAreaValue, setTextAreaValue] = useState([]);
    const [errorCode, setErrorCode] = useState();
    
    return (
        <Container fluid style={{textAlign: 'left'}}>
            <Row>
                <Col xs={3}>
                    <h1>Income</h1>
                    <h4>Date from</h4>
                    <DatePicker selected={dateFrom} onChange={date => {console.log(date); setDateFrom(date);}} />
                    <h4>Date to</h4>
                    <DatePicker selected={dateTo} onChange={date => {console.log(date); setDateTo(date)}} />
                    <Row style={{marginLeft: '0px', marginTop: '20px'}}>
                        <Button variant='contained' color='primary' onClick={() => {
                            console.log('button:');
                            console.log(dateFrom);
                            console.log(dateTo);
                            getIncome(dateFrom, dateTo)
                                .then(res => {
                                    setErrorCode(res.status)
                                    if (res.status == '200') {
                                        setTextAreaValue(res.data);
                                    }
                                    else {
                                        setTextAreaValue(res.status + res.data);
                                    }
                                })
                                .catch(err => {setErrorCode(500); setTextAreaValue(err);})
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
                    <Row>
                        <h3>Diagram:</h3><br/>
                    </Row>
                    <Row>
                        <LineChart width={1000} height={400} data={textAreaValue}>
                            <XAxis dataKey="date" name="Date"/>
                            <YAxis domain={['dataMin - 0.3', 'dataMax + 0.4']}/>
                            <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
                            <Tooltip/>
                            <Legend verticalAlign="top" height={36}/>
                            <Line type="linear" dot={false} dataKey="profit_usd" stroke="#27165c" name="Profit USD"/>
                            <Line type="linear" dot={false} dataKey="profit_pln" stroke="red" name="Profit PLN"/>
                        </LineChart>
                    </Row>
                </Col>
            </Row>
        </Container>
    )
}
