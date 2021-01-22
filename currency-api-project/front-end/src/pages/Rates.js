import React, {useState} from 'react';
import DatePicker from 'react-datepicker';
import {Container, Col, Row} from 'react-bootstrap';

import "react-datepicker/dist/react-datepicker.css";
import { Button } from '@material-ui/core';

export default function Rates() 
{
    const [startDateFrom, setStartDateFrom] = useState(new Date());
    const [startDateTo, setStartDateTo] = useState(new Date());
    
    return (
        <Container fluid style={{textAlign: 'left'}}>
            <Row>
                <Col xs={3}>
                    <h1>Rates</h1>
                    <h4>Date from</h4>
                    <DatePicker selected={startDateFrom} onChange={date => {console.log(date); setStartDateFrom(date);}} />
                    <h4>Date to</h4>
                    <DatePicker selected={startDateTo} onChange={date => setStartDateTo(date)} />
                    <Row style={{marginLeft: '0px', marginTop: '20px'}}>
                        <Button variant='contained' color='primary' onClick={() => {
                            console.log('button:')
                            console.log(startDateFrom)
                            console.log(startDateTo)
                            // todo call localhost:5000
                        }}>Try it out</Button>
                    </Row>
                </Col>
                <Col>
                    <Row>
                        <h3>JSON response:</h3><br/>
                    </Row>
                    <Row>
                        // TODO
                    </Row>
                    <Row>
                        <h3>Diagram:</h3><br/>
                    </Row>
                    <Row>
                        // TODO
                    </Row>
                </Col>
            </Row>
        </Container>
    )
}
