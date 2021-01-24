const SERVER_URL = 'http://127.0.0.1:5000';
const TABLES_URI = '/api/v1/exchangerates/tables/';
const RATES_URI = '/api/v1/exchangerates/rates/';
const SALES_URI = '/api/v1/sales/';
const DATABASE_FROM = '2014-10-16';
const RATES_TO = '2020-12-16';
const SALES_TO = '2016-12-29';
const INITIAL_CONTENT = 'sales';
const INITIAL_DATE_TO = SALES_TO;
const INITIAL_CURRENCY = 'USD';
const CURRENCY_CODES = ["USD"];


var chart_container = document.getElementById('demo_chart');
var chart_context = chart_container.getContext('2d');
var demo_chart = new Chart(chart_context,
{
    type: 'line',
    data: {},
    options:
    {
        title:
        {
            display: true,
            text: INITIAL_CONTENT
        },
        scales:
        {
            xAxes:
            [
                {
                    scaleLabel:
                    {
                        display: true,
                        labelString: 'data'
                    }
                }
            ],
            yAxes:
            [
                {
                    scaleLabel:
                    {
                        display: true,
                        labelString: ''
                    }
                }
            ]
        }
    }
});

function produce_dataset_draft(label, hue)
{
    let dataset =
    {
        label: [label],
        data: [],
        backgroundColor: 'hsla(' + hue + ', 100%, 55%, 0.2)',
        borderColor: 'hsla(' + hue + ', 70%, 50%, 1)',
        fill: false,
        borderWidth: 1,
        lineTension: 0,
        pointRadius: 0
    };

    return dataset;
}

function update_chart(chart_data, content, currency_code)
{
    var labels = [];
    demo_chart.data.datasets = [];
    demo_chart.options.title.text = content;

    if(content === "rates")
    {
        let dataset = produce_dataset_draft(currency_code, 0);
        dataset.fill = true;

        for (var i = 0; i < chart_data.length; i++)
        {
            labels.push(chart_data[i].date);
            dataset.data.push(chart_data[i].rate.toFixed(4));
        }

        demo_chart.data.datasets.push(dataset);
    }
    else
    {
        let dataset_CUR = produce_dataset_draft(currency_code, 90);
        let dataset_PLN = produce_dataset_draft('PLN', 30);

        for (var i = 0; i < chart_data.length; i++)
        {
            labels.push(chart_data[i].date)
            dataset_CUR.data.push(chart_data[i][currency_code].toFixed(2));
            dataset_PLN.data.push(chart_data[i].PLN.toFixed(2));
        }

        demo_chart.data.datasets.push(dataset_CUR);
        demo_chart.data.datasets.push(dataset_PLN);
    }

    demo_chart.data.labels = labels;
    demo_chart.update();
}


var chart = new Vue
({
    el: '#app',
    delimiters : ['[[', ']]'],
    data:
    {
        api_data:
        {
            rates: [],
            sales: []
        },
        chart_data: [],
        content: INITIAL_CONTENT,
        min_date_from: DATABASE_FROM,
        date_from: DATABASE_FROM,
        date_to: INITIAL_DATE_TO,
        currency_code: INITIAL_CURRENCY,
        currency_codes: CURRENCY_CODES,
        updated: false
    },
    computed:
    {
        max_date_to: function () { return (this.content === "rates") ? RATES_TO : SALES_TO; }
    },

    methods:
    {
        update_content: function()
        {
            let source = (this.content === "rates") ? this.api_data.rates : this.api_data.sales;
            let start = source.findIndex(item => item.date == this.date_from);
            let end = source.findIndex(item => item.date == this.date_to);
            this.chart_data = source.slice(start, end + 1);
            // alert(start + ' ' + end)
            // switch plot display
            if(start >= end) chart_container.classList.add("hidden");
            else
            {
                chart_container.classList.remove("hidden");
                update_chart(this.chart_data, this.content, this.currency_code);
            }
        },

        switch_content: function()
        {
            this.content = (this.content === "rates") ? "sales" : "rates";
            this.update_content();
        },

        refresh: function()
        {
            this.get_rates(this.currency_code, DATABASE_FROM, RATES_TO);
            this.get_sales(this.currency_code, DATABASE_FROM, SALES_TO);
        },

        get_rates: function(currency_code, date_from, date_to)
        {
            axios
                .get(SERVER_URL + RATES_URI + currency_code + '/' + date_from + '/' + date_to)
                .then(response =>
                {
                    this.api_data.rates = response.data;
                    this.update_content();
                })
                .catch(error => console.log(error))
        },

        get_sales: function(currency_code, date_from, date_to)
        {
            axios
                .get(SERVER_URL + SALES_URI + date_from + '/' + date_to)
                .then(response =>
                {
                    this.api_data.sales = response.data;
                    this.update_content();
                })
                .catch(error => console.log(error))
        }
    },

    mounted () { this.refresh(); }

});

// nie robić wykresu dla 1 punktu
