import React from 'react'
import {Table} from 'react-bootstrap'
import '../Styles.css'
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';

function RatesResults({resultApi}) {
    if (resultApi.length === 0) {
        return <RatesError error="" />
    } else if (resultApi[0].ERROR !== undefined) {
        return <RatesError error={resultApi[0].ERROR} />
    } else {
        return (
            <div>
                <RatesChart data={resultApi} />
                <RatesTable result={resultApi} />
            </div>
        )
    }
}

function RatesChart({data}) {
    return (
        <div>
            <LineChart width={1000} height={300} data={data} margin={{ top: 5, right: 20, bottom: 75, left: 0 }}>
                <Line name="USD TO PLN rate" type="monotone" dataKey="rate" stroke="#0000CD" />
                <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                <XAxis dataKey="date" angle={-45} textAnchor="end" padding={{ left: 10, right: 10 }}/>
                <YAxis dataKey="rate" domain={[1, 4]}/>
                <Tooltip />
            </LineChart>
        </div>
    )
}

function RatesTable({result}) {
    return (
        <div>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Rate</th>
                        <th>Interpolated</th>
                    </tr>
                </thead>
                <tbody>
                    {result.map((array) => {
                        return (
                            <tr>
                                <td>{array['date'] ? array['date'] : "2007-02-16"}</td>
                                <td>{array['rate'] ? array['rate'] : "2.9769"}</td>
                                <td>{array['interpolated'] ? "True" : "False"}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </Table>
        </div>
    )
}

function RatesError({error}) {
    console.log(error)
    return (
        <div>
            <h2 className="error">{error}</h2>
        </div>
    )
}

export default RatesResults
