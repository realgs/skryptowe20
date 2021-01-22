import React from 'react'
import { Typography } from 'antd';

const { Title, Text, Paragraph } = Typography;

export default function Readme() {
    const sample_rates_output = "{ \"currency\":\"USD\", \"rates\":[{\"date\":\"2020-12-01\",\"value\":\"3.736\",\"interpolated\":\"false\"},{\"date\":\"2020-12-02\",\"value\":\"3.87\",\"interpoalted\":\"false\"}]}"

    const sample_summary_output = "{\"currency\":\"USD\",\"data\":[{\"date\":\"2016-02-18\",\"original_sum\":\"202602.31\",\"currency_sum\":\"51401.03\"},{\"date\":\"2016-02-19\",\"original_sum\":\"342352.03\",\"currency_sum\":\"86603.43\"}]}"
    const sample_error_output = "{\"error\":\"Incorrect date\"}"

    return (
        <>
            <Title level={2}>API Reference</Title>
            <Title level={3}>Installation</Title>
            <p>
                <Text>
                    Make sure you have node.js installed if you plan on starting up the frontend server.
                </Text>
            </p>
            <p>
                <Text>
                    <p>Backend requires following python packages to work:</p>
                    asgiref==3.3.1
                    <br />certifi==2020.12.5
                    <br />chardet==3.0.4
                    <br />Django==3.1.4
                    <br />djangorestframework==3.12.2
                    <br />idna==2.10
                    <br />pytz==2020.4
                    <br />requests==2.25.0
                    <br />sqlparse==0.4.1
                    <br />urllib3==1.26.2
                    <p>All above packages are listed in requirements.txt, ready to be imported with python.</p>
                </Text>
            </p>
            <Title level={3}>Setup</Title>
            <Title level={4}>Preparing the database</Title>
            <Text>
                <p>1. Download <a href="https://github.com/jpwhite3/northwind-SQLite3/blob/master/Northwind_large.sqlite.zip">Northwind sqlite3 database</a>. <br />
                    2. Make sure the path to the database is correct in <i>constants.py</i><br />
                    3. The database will prepare on start of the server (as well as collect and calculate all neccessary data)</p>
            </Text>
            <Title level={4}>Starting the API server</Title>
            <Text>
                <p>1. Run manage.py located in <i>Lab5/myApi</i> with runserver argument, like so:</p>
                <i><Paragraph copyable>python manage.py runserver</Paragraph></i>
                <p>(optional) To start the frontend server go to <i>Lab5/frontend</i> and use:</p>
                <i><Paragraph copyable>npm start</Paragraph></i>
            </Text>
            <Title level={3}>Usage</Title>
            <Title level={4}>Exchange rates history</Title>
            <Text>
                <p>Data is fetched from nbpAPI. Supports all currencies supported by nbpAPI (listed in <i>constants.py</i>).
                    API endpoint url:</p>
                <i><Paragraph copyable>/rates/{"{currency}"}/{"{start_date}"}/{"{end_date}"}</Paragraph></i>
                <p>Where:</p>
                <b>currency</b> - supported currency code, specified as <b>SUMMARY_SUPPORTED_CURRENCIES</b> in <i>constants.py</i> <br />
                <b>start_date</b> - beginning of period, in format YYYY-MM-DD, <br />
                <b>end_date</b> - end of period, in format YYYY-MM-DD
                    <p>Example usage: <i>/rates/USD/2020-01-01/2020-10-10/</i></p>
                <p>Sample output:</p>
                <p><i>{sample_rates_output}</i></p>
                <p>Where:</p>
                <b>interpolated</b> - whether the value is estimated from previous days or not.
                </Text>

            <Title level={4}>Transactions summary</Title>
            <Text>
                <p>Data is calculated during database preparation on setup. Due to used database's dataset,
                         the date is bounded between 2012-07-04 and 2016-02-19 (listed in <i>constants.py</i>).</p>
                <i><Paragraph copyable>/summary/{"{currency}"}/{"{start_date}"}/{"{end_date}"}</Paragraph></i>
                <p>Where:</p>
                <b>currency</b> - supported currency code, specified as <b>SUMMARY_SUPPORTED_CURRENCIES</b> <i>constants.py</i> <br />
                <b>start_date</b> - beginning of period, in format YYYY-MM-DD, <br />
                <b>end_date</b> - end of period, in format YYYY-MM-DD
                    <p>Example usage: <i>/summary/USD/2016-02-18/2016-02-19/</i></p>
                <p>Sample output:</p>
                <p><i>{sample_summary_output}</i></p>
                <p>Where:</p>
                <b>original_sum</b> - sum of all transactions in the original value. <br />
                <b>currency_sum</b> - sum of all transactions in the requested currency.
                </Text>
            <Title level={3}>Errors</Title>
            <Text>
                <p>When status 404 is returned it means something went wrong. Example message returned stating the error:</p>
                <p><i>{sample_error_output}</i></p>
                <p>Currently, these are the supported error messages:</p>
                <b>Incorrect date</b> - input date format is not correct <br />
                <b>No data for this period</b> - you requestes summary out of the bounded period <br />
                <b>Unsupported currency</b> - currency is not on supported currencies list <br />
                <b>Incorrect input</b> - other input error <br />
                <b>Start date should be smaller than end date</b> - start date should be smaller than end date <br />
                <b>Internal database error</b> - something went wrong with database connection within our system<br />
                <b>Requests limit reached</b> - limit of requests per minute was reached <br />
                <b>Failed to fetch from NBPAPI</b> - error connecting with NBPAPI
                </Text>
            <Title level={3}>Requests limit</Title>
            <Text>
                Requests are limited to <i><b>100 requests per minute for everyone</b></i>. The value can be changed by updating <b>MAX_REQ_PER_MINUTE</b> in <i>constants.py</i>.
                </Text>
        </>
    )
}
