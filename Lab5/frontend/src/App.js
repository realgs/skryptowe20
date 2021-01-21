import React from 'react'
import './App.css';
import RatesTable from './RatesTable'
import { Layout } from 'antd';
import { Button } from 'antd';
import { Typography } from 'antd';
import { DatePicker} from 'antd';

const { RangePicker } = DatePicker;
const { Title, Text } = Typography;
const { Header, Footer, Sider, Content } = Layout;

function fetchRates(currency, start_date, end_date) {
    return fetch("http://127.0.0.1:8000/rates/" + currency + "/" +  start_date + "/" + end_date + "/")
}

function convertDate(date) {
    if (date == null) return null;

    var start_date_obj = new Date(date);
    var year = start_date_obj.getFullYear();
    var month = start_date_obj.getMonth()+1;
    var day = start_date_obj.getDate();
    var output = "";

    output += year;
    output+="-"
    if(month < 10) {
        output += "0" + month;
    } else {
        output += month;
    }
    output+="-"
    if(day < 10) {
        output += "0" + day;
    } else {
        output += day;
    }

    return output;
}

class App extends React.Component {
    state = {
        currency:"",
        rates:[]
    }

    range_dates = {
        start_date:null,
        end_date:null
    }

    registerButtonClick = () => {
        var start_date = convertDate(this.range_dates.start_date);
        var end_date = convertDate(this.range_dates.end_date);

        if(start_date == null || end_date == null) return;

        fetchRates("USD", start_date , end_date).then(result => result.json())
                       .then(json => {
                           var error = json['error'];
                           if(error != null) {
                                this.setState({
                                    currency: error,
                                    rates: []
                                })
                           } else {
                                this.setState({
                                    currency: json['currency'],
                                    rates: json['rates']
                                })
                           }

                       });
    }

    setDateRange = dates => {
        if(dates == null) return;
        this.range_dates.start_date = dates[0];
        this.range_dates.end_date = dates[1];
    }

    render() {
        return (
            <div className="App">
                <Layout>

                    <Header>
                      <Title>Moja super webapp</Title>
                    </Header>

                    <Layout>

                    <Sider>
                       <Title level={4}>Opcje</Title>
                       <RangePicker onChange={ this.setDateRange } />

                       <Button type="primary" onClick={ this.registerButtonClick }>Przycisk</Button>
                    </Sider>

                    <Content>
                      <Title level={4}>Rezultat</Title>
                      <RatesTable data={ this.state }/>
                    </Content>

                    </Layout>

                    <Footer>
                    <Text>All rights reserved C</Text>
                    </Footer>

                </Layout>
            </div>
        )
    }
}

export default App;
