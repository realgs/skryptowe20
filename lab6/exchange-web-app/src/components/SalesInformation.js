import React, {useEffect, useRef, useState} from 'react';

const TODAY_DATE = new Date().toISOString().slice(0, 10);

export default function SalesInformation() {

    const [currency, setCurrency] = useState('USD');
    const [date, setDate] = useState(new Date(2019, 1, 1).toISOString().slice(0, 10));
    const [response, setResponse] = useState(null);
    const [isLoading, setIsLoading] = useState(true)
    const [isError, setIsError] = useState(false)
    const isFirstRender = useRef(true)

    useEffect(() => {
        if (!isFirstRender.current) {
            callExchanges();
        }
    }, [date, currency])

    useEffect(() => {
        isFirstRender.current = false
    }, [])

    function callExchanges() {
        setIsLoading(true);
        fetch(`http://localhost:8080/api/sales/${currency}?date=${date}`, {
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
            return (<div className="alert alert-danger text-start m-5" role="alert">
                <h4 className="alert-heading">Error!</h4>
                <p>There was an error while connecting to exchange api.</p>
                <hr/>
                <p className="mb-0">Please try again later.</p>
            </div>);
        } else if (isLoading) {
            return (<div className="spinner-border text-dark mt-5" role="status">
                <span className="visually-hidden">Loading...</span>
            </div>);
        } else {
            return (
                <div className="shadow card">
                    <h4 className="card-header">{date} Sales</h4>
                    <ul className="list-group list-group-flush">
                        <li className="list-group-item">
                            <strong>{parseFloat(response.totalOrdersAmountInPLN).toFixed(2)} PLN</strong>
                        </li>
                        <li className="list-group-item">
                            <strong>{parseFloat(response[`totalOrdersAmountIn${currency}`]).toFixed(2) + ' ' + currency}</strong>
                        </li>
                    </ul>
                </div>
            );
        }
    }

    return (
        <div>
            <div style={{height: 25, margin: 10}}>
            <span className="float-start">
                <input type="date" id="start" name="trip-start" value={date} min="2012-01-01"
                       max={TODAY_DATE}
                       onChange={event => setDate(event.target.value)}
                />
            </span>
                <span className="float-end">
                  <select
                      id="inputState"
                      onChange={event => setCurrency(event.target.value)}
                      defaultValue='EUR'
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
            <div style={{paddingRight: 20, paddingLeft: 20}}>
                {generateBody()}
            </div>
        </div>
    );
}