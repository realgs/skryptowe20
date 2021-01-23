<template>
  <div class="homepage">
    <h1>Projekt z języków skryptowych</h1>
    <h2>Kursy wymiany</h2> <br>
    <p>
        Korzystając z poniższych kontrolek, możesz wybrać daty, dla których chcesz uzyskać kursy wymiany dolara na złotówki. Dodtkowe informacje:
        <ul>
            <li>Zachowany z poprzedniego dnia - ta kolumna informuje o tym, czy kurs jest nowy, czy został pobrany z poprzedniego dnia (w przypadku weekendów i świąt).</li>
            <li>Dostępne są dane dla dat z przedziału 01.01.2014 - 31.12.2015 </li>
        </ul>
    </p>

    <p>
      <label for="start">Data początkowa:</label> <br>

      <input type="date" id="startDate" 
        v-model="startDate"
        :min=this.limits.minDate 
        :max=this.endDate>
        <!-- pamietaj o walidacji, by byla mniejsza od daty koncowej --> <br>
    </p>

    <p>
      <input type="checkbox" 
        id="rangeCheckbox" 
        name="range" 
        value="range" 
        v-model="range"  > 
      <label for="range"> Przedział dat</label><br>
    </p>

    <p>
      <label for="start" >Data końcowa:</label> <br>
      <input type="date" id="endDate"
        v-model="endDate"
        :disabled="range == 0"
        :min=this.startDate
        :max=this.limits.maxDate> <br>
    </p>

    <button v-on:click="getExchangeRates()">Pobierz dane</button> <br>

    <!-- <button v-on:click="counter += 1">Add 1</button> -->
    <h2>Kursy:</h2>
    <table>
      <thead>
        <td>Data</td>
        <td>Kurs dolara</td>
        <td>Zachowany z poprzedniego dnia</td>
      </thead>
      <tbody>
        <tr v-for="rate in exchangeRates" :key="rate._id">
          <td>{{ rate.date }}</td>
          <td>{{ rate.pln_to_usd }}</td>
          <td>{{ rate.interpolated ? "Tak" : "Nie" }}</td>
        </tr>
      </tbody>
    </table>
    
    <div class="chart" v-if="this.chart.show">
      <h2>Wykres:</h2>
      <line-chart :chart-data="chart.data" :chartOptions="chart.options"></line-chart>
    </div>

  </div>
  
</template>

<script>
import axios from 'axios';
import LineChart from './LineChart.js'

export default {
  name: 'ExchangeRates',
  components: {
    LineChart
  },
  data() {
    return {
      limits: {
        minDate: '2014-01-01',
        maxDate: '2015-12-31'
      },
      chart:{
        show: false,
        data: null,
        options: {maintainAspectRatio: false, responsive: true},
      },
      exchangeRates: [],
      startDate: '2014-01-01',
      endDate: '2015-12-31',
      range: false,
    }
  },
  created() {
  },
  beforeDestroy() {
    clearInterval(this.setIntervalId);
  },
  methods: {
    async getExchangeRates() {
      try {
        if (this.range){
          const exchangeRates = await axios.get(`http://127.0.0.1:8000/api/exchangerates/${this.startDate}/${this.endDate}`);
          this.exchangeRates = exchangeRates.data.exchange_rates;
        }
        else {
          const exchangeRates = await axios.get(`http://127.0.0.1:8000/api/exchangerates/${this.startDate}`);
          this.exchangeRates = [exchangeRates.data];
        }
      } catch(err) {
        console.log(err);
      }

      if (this.range) {
        this.prepareChartData();
        this.chart.show = true;
      }
      else{
        this.chart.show = false;
      }
    },
    async prepareChartData(){
      this.chart.data = {
        labels: this.exchangeRates.map((R) => R.date),
        datasets: [
          {
            label: 'USD',
            borderColor: '#228B22',
            borderWidth: 3,
            lineTension: 0,
            pointRadius: 3,
            data: this.exchangeRates.map((R) => R.pln_to_usd),
          },
        ],
      };
    }
  }
}


</script>

<style scoped>
h3 {
    margin: 40px 0 0;
}
li {
    list-style-type: none;
    margin: 0 10px;
}
a {
    color: #42b983;
}
th div { margin-top: -20px; position: absolute; }
table  {  
  border: 1px solid #13b4fd;
  margin-top: 20px; 
  display: inline-block; 
  overflow: auto; 
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  max-height: 200px;
}
table td {
	padding: 5px;
	border: 1px solid #13b4fd;
}

.chart {
  width: 100%;
  height: 10%;
  margin: 40px 0 0;
}
 
</style>
