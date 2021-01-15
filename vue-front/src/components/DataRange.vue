<template>
<v-container fill-height>
<v-row  class="mt-2" justify="center">
<v-col
      cols="12"
      sm="6"
      md="3"
      offset-md="1"
    >
      <v-menu
        ref="start_picker"
        v-model="start_picker"
        :close-on-content-click="false"
        :return-value.sync="date_start"
        transition="scale-transition"
        offset-y
        min-width="auto"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            v-model="date_start"
            label="Pick start date"
            prepend-icon="mdi-calendar"
            readonly
            v-bind="attrs"
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker
          v-model="date_start"
          no-title
          scrollable
          show-current="2003-05-05"
          min="2003-05-05"
          max="2005-05-05"
        >
          <v-spacer></v-spacer>
          <v-btn
            text
            color="primary"
            @click="start_picker = false"
          >
            Cancel
          </v-btn>
          <v-btn
            text
            color="primary"
            @click="$refs.start_picker.save(date_start)"
          >
            OK
          </v-btn>
        </v-date-picker>
      </v-menu>
    </v-col>
    <v-col
      cols="12"
      sm="6"
      md="3"
    >
      <v-menu
        ref="end_picker"
        v-model="end_picker"
        :close-on-content-click="false"
        :return-value.sync="date_end"
        transition="scale-transition"
        offset-y
        min-width="auto"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            v-model="date_end"
            label="Pick end date"
            prepend-icon="mdi-calendar"
            readonly
            v-bind="attrs"
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker
          v-model="date_end"
          no-title
          scrollable
          show-current="2005-05-05"
          min="2003-05-05"
          max="2005-05-05"
        >
          <v-spacer></v-spacer>
          <v-btn
            text
            color="primary"
            @click="end_picker = false"
          >
            Cancel
          </v-btn>
          <v-btn
            text
            color="primary"
            @click="$refs.end_picker.save(date_end)"
          >
            OK
          </v-btn>
        </v-date-picker>
      </v-menu>
    </v-col>
    <v-col   
      cols="12"
      sm="6"
      md="4"
      align="center">
    <v-btn
      class="ma-2"
      @click="getData"
      color="secondary"
    >
      Generate      
    </v-btn>
    </v-col>
  </v-row>
  <v-row
  no-gutters>
    <v-col   
    class="ma-2" 
      align="center">
        <section v-if="errored" align="center" style="color:red; font-size:18px; font-weight:bold">
            <p>API responded with code {{error_msg}}</p>
      </section>
        <Chart :chartdata="chartdata" :options="options" chartLabel="label" v-if="chartdata !== null "/>
    </v-col>
  </v-row>
  <v-row>
    <v-col   
      align="center">
    <v-card v-if="active && !errored">
    <v-card-title>
      {{title}}
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="responseToList"
      :search="search"
    ></v-data-table>
  </v-card>
    </v-col>
  </v-row>

</v-container>
</template>

<script>
import axios from "axios";
import Chart from "./Chart"

export default {
    name: "DataRange",

    components: {
      Chart
  },
  computed:{
    responseToList: function(){
      let vals = [];
      for(var key in this.response)
        vals.push(this.response[key]);
      console.log(vals); 
      return vals;  
    }
  },
    data: () => ({
      start_picker: false,
      search: '',
      chartdata:null,
      options:null,
      end_picker: false,
      response:null,
      errored:false,
      active:false,
      error_msg:"",
      date_end: null,
      date_start: null,
      headers:null,
      title:"",
      sales_headers:[
        {text:'Date', value: 'date'},
        {text:'USD rate', value: 'usd_rate'},
        {text:'Sale in PLN', value: 'pln_sale_sum'},
        {text:'Sale in USD', value: 'usd_sale_sum'},
      
      ],
      rates_headers:[
        {text:'Date', value: 'date'},
        {text:'Interpolated', value: 'interpolated'},
        {text:'USD rate', value: 'usd_rate'},  
      ],
      options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
              yAxes: [{
                  scaleLabel: {
                      display: true,
                      labelString: ""
                  },
                  ticks: {
                    maxTicksLimit: 15,
                    autoSkip: true
                  }
              }],
              xAxes: [{
                  scaleLabel: {
                      display: true,
                      label: "",
                  },
                  ticks: {
                    maxTicksLimit: 15,
                    autoSkip: true
                  }
              }]
          }
        },
    }),
    props:["url"],
    methods: {
      async requestForRange() {
        await axios.get(`http://127.0.0.1:5000/${this.url}/${this.date_start}/${this.date_end}`,{responseType: 'json'})
        .then((resp) =>(this.response = resp.data))
        .catch((e) => {
          console.log(e);  
          this.errored = true
          this.error_msg = e.response.status + ":   " + e.response.data;

        });
        this.active=true;
        if (this.url == 'rates'){
          this.renderRatesChart();
          this.headers= this.rates_headers;
          this.title="Rates Data";

        }
        else if (this.url == 'sales'){
          this.renderSalesChart();
          this.headers = this.sales_headers;
          this.title="Sales Data";
        }
        
    },
    getData(){
      if(this.datesValid()){
         this.resetDisplay();
         this.requestForRange();
      }
      else            
        alert('Start date must be smaller than end date');
    },
    renderRatesChart() {
      let dates = [];
      let rates = [];
      for (var key in this.response) {
        dates.push(this.response[key].date)
        rates.push(this.response[key].usd_rate)
      }
        this.chartdata = {
          labels: dates,
          datasets: [{
              label: "USD Exchange Rates Chart",
              borderColor: '#492cf2',
              pointBackgroundColor: '#000000',
              data: rates,
              fill: true
            }
          ]
        }
        this.options.scales.yAxes[0].scaleLabel.labelString = "USD Exchange rate";
        this.options.scales.xAxes[0].scaleLabel.labelString = "Date";
    },
    renderSalesChart() {
      let sales_PLN = [];
      let sales_USD = [];
      let dates = [];
      for (var key in this.response) {
        dates.push(this.response[key].date) 
        sales_PLN.push(this.response[key].pln_sale_sum);
        sales_USD.push(this.response[key].usd_sale_sum);
        this.chartdata = {
          labels: dates,
          datasets: [{
              label: "Sale Values in PLN",
              borderColor: '#04661b',
              pointBackgroundColor: '#000000',
              data: sales_PLN,
              fill: false
            },
            {
              label: "Sale  Values in USD",
              borderColor: '#492cf2',
              pointBackgroundColor: '#000000',
              data: sales_USD,
              fill: true
            }
          ]
        };
        this.options.scales.yAxes[0].scaleLabel.labelString = "Sales value";
        this.options.scales.xAxes[0].scaleLabel.labelString = "Date";
      }
    },
    datesValid() {
      return this.date_start<this.date_end;
    },
    resetDisplay(){
      this.response=null;
      this.chartdata=null;
      this.errored=false;
      this.error_msg="";
      this.active=false;
      this.headers=null;
    }
    },
  }
</script>