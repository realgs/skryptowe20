<template>
  <div class="homepage">
    <h1>Projekt z języków skryptowych</h1>
    <h2>Wartość sprzedaży</h2> <br>
    <p>
        Korzystając z poniższych kontrolek, możesz wybrać daty, dla których chcesz uzyskać wartość transakcji z bazy danych w PLN i USD. <br>
        <ul>
            <li>Dostępne są dane dla dat z przedziału 01.01.2014 - 31.12.2015 </li>
        </ul>
    </p>

    <p>
      <label for="start">Data początkowa:</label> <br>

      <input type="date" id="startDate" 
        v-model="startDate"
        :min=this.limits.minDate 
        :max=this.endDate>
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

    <button v-on:click="getRates()">Pobierz dane</button> <br>

    <h2>Kursy:</h2>
    <table>
      <thead>
        <td>Data</td>
        <td>Wartość w PLN</td>
        <td>Wartość w USD</td>
      </thead>
      <tbody>
        <tr v-for="rate in rates" :key="rate._id">
          <td>{{ rate.date }}</td>
          <td>{{ rate.pln }}</td>
          <td>{{ rate.usd }}</td>
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
  name: 'Transactions',
  components: {
    LineChart
  },
  data() {
    return {
      limits: {
        minDate: '2014-01-02',
        maxDate: '2015-12-31'
      },
      chart:{
        show: false,
        data: null,
        options: {maintainAspectRatio: false, responsive: true},
      },
      rates: [],
      startDate: '2014-01-02',
      endDate: '2015-12-31',
      range: false,
    }
  },
  methods: {
    async getRates() {
      try {
        if (this.range){
          const rates = await axios.get(`http://127.0.0.1:8000/api/transactions/${this.startDate}/${this.endDate}`);
          this.rates = rates.data.transactions;
        }
        else {
          const rates = await axios.get(`http://127.0.0.1:8000/api/transactions/${this.startDate}`);
          this.rates = [rates.data];
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
        labels: this.rates.map((R) => R.date),
        datasets: [
          {
            label: 'PLN',
            borderColor: '#FF0000',
            borderWidth: 3,
            lineTension: 0,
            pointRadius: 3,
            data: this.rates.map((R) => R.pln),
          },
                    {
            label: 'USD',
            borderColor: '#62812A',
            borderWidth: 3,
            lineTension: 0,
            pointRadius: 3,
            data: this.rates.map((R) => R.usd),
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
table  {  
  border: 1px solid #13b4fd;
  margin-top: 20px; 
  display: inline-block; 
  overflow: auto; 
  width: 100%;
  max-width: 400px;
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
