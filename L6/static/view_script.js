const START_LINK = 'http://127.0.0.1:5000/api/v1/';
const EXCHANGERATES_LINK = 'exchangerates/USD/';
const SALES_LINK = 'salesdata/';
const CHART_ID = 'myChart';
const FORM_DEFAULT_START_DATE = '2015-01-01';
const FORM_DEFAULT_END_DATE = '2015-12-31';
const DELIMITERS = ['[[', ']]'];
const ERR_DESCRIPTION_400 = '400 BadRequest - Błędny zakres dat';
const ERR_DESCRIPTION_404 = '404 NotFound - Brak danych (możliwy zakres to 2013-2016)';
const ERR_DESCRIPTION_429 = '429 Too Many Requests - Zbyt wiele zapytań (limit: 10/min - spróbuj ponownie później)';
const ERR_DESCRIPTION_DEFAULT = 'Nieznany błąd';


var myChart = document.getElementById(CHART_ID);
myChart.style.display = 'none';

var ctx = document.getElementById(CHART_ID).getContext('2d');
var chart = new Chart(ctx, {
    type: 'line',
    data: {},
    options: {
      title: {
        display: true,
        text: 'Empty chart'
      },
      scales: {
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'data'
          }
        }],
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: ''
          }
        }]
      }    
    }
});

function update_chart(){
  chart.update();
  if(chart.data.labels.length <= 1) myChart.style.display = 'none';
  else myChart.style.display = 'block';
}

function prepare_chart(title, yLabel, datasets){
  chart.options.title.text = title;
  chart.options.scales.yAxes[0].scaleLabel.labelString = yLabel;
  chart.data.datasets = datasets;
  chart.data.datasets.forEach(dataset => {
    dataset['data']=[],
    dataset['fill']=false,
    dataset['lineTension']=0,
    dataset['pointRadius']=0
  });
  chart.data.labels = [];
}

function generate_exchangerates_chart(data){
  var datasets = [{
    label: 'USD',
    backgroundColor: 'rgb(255, 99, 132)',
    borderColor: 'rgb(255, 99, 132)',
  }];
  prepare_chart('Średni kurs dolara', 'śr. kurs [PLN]', datasets);
  data.forEach(element => {
    chart.data.datasets[0].data.push(element['rate']);
    chart.data.labels.push(element['date']);
  });
  update_chart();
}

function generate_sales_chart(data){
  var datasets = [
    { label: 'USD',
      borderColor: 'rgb(122, 99, 132)',
      backgroundColor: 'rgb(122, 99, 132)',
    },
    { label: 'PLN',
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: 'rgb(255, 99, 132)',
    }            
  ];
  prepare_chart('Łączna sprzedaż', 'wartość sprzedanych towarów', datasets);
  data.forEach(element => {
    chart.data.datasets[1].data.push(element['PLN'].toFixed(2));
    chart.data.datasets[0].data.push(element['USD'].toFixed(2));
    chart.data.labels.push(element['date']);
  });
  update_chart();
}

function describe_error_codes(status){
  var description = '';
  switch (status) {
    case 400:
      description = ERR_DESCRIPTION_400;
      break;
    case 404:
      description = ERR_DESCRIPTION_404;
      break;
    case 429:
      description = ERR_DESCRIPTION_429;
      break;
    default:
      description = ERR_DESCRIPTION_DEFAULT;
      break;
    }
  return description;
}

var exchangerates_table = new Vue({
  el: '#exchangerates_table',
  delimiters : DELIMITERS,
  data: {
    start_date : FORM_DEFAULT_START_DATE,
    end_date : FORM_DEFAULT_END_DATE,
    data_option : "",
    theads: [],
    keys: [],
    error_message : '',
    exchangerates_keys: [
      'date',
      'rate',
      'interpolated'
    ],
    sales_keys: [
      'date',
      'PLN',
      'USD'
    ],
    exchangerates_theads: [
      'Data notowania',
      'Kurs dolara',
      'Przybliżenie'
    ],
    sales_theads: [
      'Data sprzedaży',
      'Sprzedaż w złotówkach',
      'Sprzedaż w dolarach'
    ],
    tbodys: []
  },
  methods: {
    clear_all : function (){
      this.tbodys = [];
      this.theads = [];
      this.keys = [];
      myChart.style.display = 'none';
    },
    update_table : function (event){
      this.error_message = ''
      if (this.data_option=='exchangerates') {
        axios
        .get(START_LINK + EXCHANGERATES_LINK + this.start_date + '/' + this.end_date)
        .then(response => {this.tbodys = response.data;
          generate_exchangerates_chart(this.tbodys);
          this.keys = this.exchangerates_keys;
          this.theads = this.exchangerates_theads;
        })
        .catch(error => {console.error(error);
          this.error_message = describe_error_codes(error.response.status);
          this.clear_all();
        });
      }
      if (this.data_option=='sales') {
        axios
        .get(START_LINK + SALES_LINK + this.start_date + '/' + this.end_date)
        .then(response => {this.tbodys = response.data;
          generate_sales_chart(this.tbodys);
          this.keys = this.sales_keys;
          this.theads = this.sales_theads;
        })
        .catch(error => {console.error(error);
          this.error_message = describe_error_codes(error.response.status);
          this.clear_all();
        });
      }
    }    
  }
});
