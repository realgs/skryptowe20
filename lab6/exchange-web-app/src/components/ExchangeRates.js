import React, {useEffect, useRef, useState} from 'react';
import ReactApexCharts from 'react-apexcharts'

const TODAY_DATE = new Date().toISOString().slice(0, 10);


export default function ExchangeRates() {

    let someDate = new Date();
    someDate.setDate(someDate.getDate() - 10);

    const [response, setResponse] = useState(null);
    const [currency, setCurrency] = useState('USD');
    const [startDate, setStartDate] = useState(someDate.toISOString().slice(0, 10));
    const [endDate, setEndDate] = useState(TODAY_DATE);
    const [isLoading, setIsLoading] = useState(true)
    const [isError, setIsError] = useState(false)
    const isFirstRender = useRef(true)

    useEffect(() => {
        if (!isFirstRender.current) {
            callExchanges();
        }
    }, [startDate, endDate, currency])

    useEffect(() => {
        isFirstRender.current = false
    }, [])

    function callExchanges() {
        setIsLoading(true);
        fetch(`http://localhost:8080/api/rates/${currency}?startDate=${startDate}&endDate=${endDate}`, {
            method: 'GET'
        }).then(res => {
            if (res.status === 200) {
                res.json().then(value => {
                    console.log(value)
                    setResponse(value)
                    setIsLoading(false)
                    if (isError) {
                        setIsError(false)
                    }
                });
            } else {
                setIsError(true)
                setIsLoading(false)
            }
        }).catch(_ => {
            setIsError(true)
            setIsLoading(false)
        })
    }

    if (isFirstRender.current) {
        callExchanges()
        isFirstRender.current = false
    }

    function generateBody() {
        if (isError) {
            return (
                <div className="alert alert-danger text-start m-5" role="alert">
                    <h4 className="alert-heading">Error!</h4>
                    <p>There was an error while connecting to exchange api.</p>
                    <hr/>
                    <p className="mb-0">Please try again later.</p>
                </div>
            );
        } else if (isLoading) {
            return (
                <div className="spinner-border text-dark mt-5" role="status">
                    <span className="visually-hidden">Loading...</span>
                </div>
            );
        } else {
            const ratesTableElements = response.rates.map((rate, index) => {
                return (<tr key={`rate-row-${index}`}>
                    <th scope="row">{rate.date}</th>
                    <td>{rate.rate} zł</td>
                </tr>)
            })
            return (
                <div style={{paddingRight: 10, paddingLeft: 10}}>
                    <ReactApexCharts options={{
                        chart: {
                            height: 350,
                            type: 'line',
                            zoom: {
                                enabled: false
                            }
                        },
                        dataLabels: {
                            enabled: false
                        },
                        title: {
                            text: `PLN to ${currency} exchange rates`,
                            align: 'left'
                        },
                        xaxis: {
                            type: 'datetime',
                            categories: response.rates.map(rate => rate.date)
                        },
                    }} series={[{
                        name: `${currency} price`,
                        data: response.rates.map(rate => rate.rate)
                    }]}
                                     type="area"
                                     height={350}/>
                    <table className="table table-sm table-hover text-start">
                        <thead className="table-dark">
                        <tr>
                            <th scope="col">Date</th>
                            <th scope="col">Rate</th>
                        </tr>
                        </thead>
                        <tbody>{ratesTableElements}</tbody>
                    </table>
                </div>)
        }
    }

    return (
        <div>
            <div style={{height: 25, margin: 10}}>
                    <span className="float-start">
                    <input type="date" id="start" name="trip-start" value={startDate} min="2012-01-01"
                           max={endDate}
                           onChange={event => setStartDate(event.target.value)}
                    /> ~ <input type="date" id="end" name="trip-start" value={endDate} min={startDate}
                                max={TODAY_DATE}
                                onChange={event => setEndDate(event.target.value)}
                    />
                    </span><span className="float-end">
                    <select
                        id="inputState"
                        onChange={event => setCurrency(event.target.value)}
                        defaultValue="EUR"
                    >
                    <option>EUR</option>
                    <option>USD</option>
                    <option>GBP</option>
                    <option>CHF</option>
                    <option>AUD</option>
                    <option>RUB</option>
                    <option>TRY</option>
                    </select>
                    </span>
            </div>
            {generateBody()}
        </div>);
}
