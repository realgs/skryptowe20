import React from 'react'
import './App.css';
import RatesTable from './RatesTable'
import { Layout, Button, Typography, DatePicker, Select } from 'antd';
import { Menu, Dropdown } from 'antd';
import { DownOutlined } from '@ant-design/icons';
const { Option } = Select;
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
        content:0,
        currency:"",
        rates:[]
    }

    range_dates = {
        start_date:null,
        end_date:null
    }

    selector_currency = {
        currency:"USD"
    }

    registerButtonClick = () => {
        var start_date = convertDate(this.range_dates.start_date);
        var end_date = convertDate(this.range_dates.end_date);

        if(start_date == null || end_date == null) return;

        fetchRates(this.selector_currency.currency, start_date , end_date).then(result => result.json())
                       .then(json => {
                           let error = json['error'];
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

    setCurrency = currency => {
        this.selector_currency.currency = currency;
    }

    setDefaultContent = () => {
        this.setState({
            content:0
        })
    }

    setRatesContent = () => {
        this.setState({
            content:1
        })
    }

    setSummaryContent = () => {
        this.setState({
            content:2
        })
    }

    render() {

        const menu = (
            <Menu>
              <Menu.Item onClick={ this.setDefaultContent }>
                  API Reference
              </Menu.Item>
              <Menu.Item onClick={ this.setRatesContent }>
                  Rates exchange
              </Menu.Item>
              <Menu.Item onClick={ this.setSummaryContent }>
                  Transactions summary
              </Menu.Item>
            </Menu>
          );


        const display_content = this.state.content;
        let content;
        let options;

        if (display_content == 1) {
            content =
            <>
                <Title level={4}>Rezultat</Title>
                <RatesTable data={ {currency:this.state.currency,
                                    rates:this.state.rates} }/>
            </>
            options =
            <>
                <RangePicker onChange={ this.setDateRange } />
                <Select defaultValue="USD" style={{ width: 80 }} onChange={this.setCurrency}>
                    <Option value="USD">USD</Option>
                    <Option value="EUR">EUR</Option>
                    <Option value="AUD">AUD</Option>
                </Select>
                <Button type="primary" onClick={ this.registerButtonClick }>Przycisk</Button>
            </>
        } else if (display_content == 2) {
            content =
            <>
            Kaczka
            </>
            options =
            <>
            </>
        } else {
            content =
            <>
            Index
            </>
            options =
            <>
            </>
        }

        return (
            <div className="App">
                <Layout>

                    <Header>
                      <Title>Moja super webapp</Title>
                    </Header>

                    <Layout>

                    <Sider>
                        <Title level={4}>Opcje</Title>
                        <Dropdown overlay={menu}>
                            <a className="ant-dropdown-link">
                            Menu <DownOutlined />
                            </a>
                        </Dropdown>
                        { options }
                    </Sider>

                    <Content>
                        {content}
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
