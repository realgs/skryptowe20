import React, {useEffect, useRef, useState} from 'react';

function ExchangeRates() {

    const today = new Date();
    const todayDate = today.toISOString().slice(0, 10);

    let someDate = new Date();
    someDate.setDate(someDate.getDate() - 10);

    const [response, setResponse] = useState({rates: []});
    const [currency, setCurrency] = useState('USD');
    const [startDate, setStartDate] = useState(someDate.toISOString().slice(0, 10));
    const [endDate, setEndDate] = useState(todayDate);
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
        fetch(`http://localhost:8080/api/rates/${currency}?startDate=${startDate}&endDate=${endDate}`, {
            method: 'GET'
        }).then(res => {
            if (res.status === 200) {
                res.json().then(value => {
                    console.log(value)
                    setResponse(value)
                })
            }
        })

    }

    if (isFirstRender.current) {
        callExchanges()
    }

    return (
        <div>
            <div style={{height: 25, margin: 10}}>
            <span className="float-start">
                <input type="date" id="start" name="trip-start" value={startDate} min="2012-01-01"
                       max={endDate}
                       onChange={event => setStartDate(event.target.value)}
                /> ~ <input type="date" id="end" name="trip-start" value={endDate} min={startDate}
                            max={todayDate}
                            onChange={event => setEndDate(event.target.value)}
            />
            </span><span className="float-end">
                  <select
                      id="inputState"
                      onChange={event => {
                          setCurrency(event.target.value);
                      }}>
                    <option selected>USD</option>
                    <option>EUR</option>
                    <option>GBP</option>
                    <option>CHF</option>
                    <option>AUD</option>
                    <option>RUB</option>
                    <option>TRY</option>
                </select>
            </span>
            </div>
            <table className="table table-sm table-hover text-start">
                <thead className="table-dark">
                <tr>
                    <th scope="col">Date</th>
                    <th scope="col">Rate</th>
                </tr>
                </thead>
                <tbody>
                {
                    response.rates.map(rate => {
                        return (<tr>
                            <th scope="row">{rate.date}</th>
                            <td>{rate.rate} zł</td>
                        </tr>)
                    })
                }
                </tbody>
            </table>

        </div>
    )
        ;
}

export default ExchangeRates;