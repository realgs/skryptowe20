import React from 'react'
import {Table} from 'react-bootstrap'
import '../Styles.css'
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';

function SalesResults({resultApi}) {
    if (resultApi.length === 0) {
        return <SalesError error="" />
    } else if (resultApi[0].ERROR !== undefined) {
        return <SalesError error={resultApi[0].ERROR} />
    } else {
        return (
            <div>
                <SalesChart data={resultApi} />
                <SalesTable result={resultApi} />
            </div>
        )
    }
}

function SalesChart({data}) {
    return (
        <div>
            <LineChart width={1000} height={300} data={data} margin={{ top: 5, right: 20, bottom: 75, left: 20 }}>
                <Line name="USD Sales" type="monotone" dataKey="sum_of_sales_in_USD" stroke="#FF7F00" />
                <Line name="PLN Sales" type="monotone" dataKey="sum_of_sales_in_PLN" stroke="#0000CD" />
                <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                <XAxis name="Date" dataKey="date" angle={-45} textAnchor="end" padding={{ left: 10, right: 10 }}/>
                <YAxis name="Sum of Sales" dataKey="sum_of_sales_in_PLN"/>
                <Tooltip />
            </LineChart>
        </div>
    )
}

function SalesTable({result}) {
    return (
        <div>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Sum of sales in USD</th>
                        <th>Sum of sales in PLN</th>
                        <th>USD to PLN rate</th>
                    </tr>
                </thead>
                <tbody>
                    {result.map((array) => {
                        return (
                            <tr>
                                <td>{array['date']}</td>
                                <td>{array['sum_of_sales_in_USD']}</td>
                                <td>{array['sum_of_sales_in_PLN']}</td>
                                <td>{array['USD_to_PLN_rate']}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </Table>
        </div>
    )
}

function SalesError({error}) {
    console.log(error)
    return (
        <div>
            <h2 className="error">{error}</h2>
        </div>
    )
}

export default SalesResults
