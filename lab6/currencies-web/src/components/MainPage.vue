<template>
  <div class="main-page">
    <div class="container">
      <div class="welcome-text">
        Welcome on currencies website!
      </div>
      <div class="description">
        On the top of the page you have two sections: data panel where you can see exchange rates and sales data, and contact panel with my github info.
        <br/>
        This website is made with vue.js! It uses axios to fetch data from currencies API deployed on heroku:
        <a href="https://currencies-api-lab6.herokuapp.com" target="_blank">https://currencies-api-lab6.herokuapp.com/</a>.
        Endpoints are described below.
        <br/>
        Source code for this api: <a href="https://github.com/szawruk/skryptowe20/tree/lab5/lab5" target="_blank">https://github.com/szawruk/skryptowe20/tree/lab5/lab5</a> and readme from git:

      </div>
      <div class="readme">
        <vue-simple-markdown :source="source"></vue-simple-markdown>
      </div>

    </div>
  </div>
</template>

<script>

export default {
  name: 'MainPage',
  computed:{
    source(){
      return "# Exchange rates api with sales data\n" +
          "\n" +
          "This application provides an API that allows to check USD exchange rates and total sale of one online store in PLN and USD.\n" +
          "\n" +
          "## What do you need?\n" +
          "\n" +
          "### a)\n" +
          "You'll need python installed on your computer. I tested this project with python 3.9. You can download it from https://www.python.org/downloads/\n" +
          "\n" +
          "### b)\n" +
          "Some python packages. All needed packages are in file requirements.txt. To install then you need to open terminal in cloned directory and type \n" +
          "```bash\n" +
          "pip install -r requirements.txt\n" +
          "```\n" +
          "\n" +
          "### c)\n" +
          "MySQL server. I recommend you XAMPP. You can get it from https://www.apachefriends.org/pl/download.html.\n" +
          "\n" +
          "### d)\n" +
          "In this repo you have db.sql file. That is database with all API data. You can import it with MySQL Workbench.\n" +
          "\n" +
          "## Project structure\n" +
          "* api.py is main file with API configuration\n" +
          "* db_service.py is file with functions that allow to work with database\n" +
          "* init.py is initial script for set up the database. If you have imported database given in repo you don't need this script.\n" +
          "* nbp.py is script that allows to fetch data from NBP API.\n" +
          "\n" +
          "## Run app\n" +
          "1. Run MySQL server with imported database\n" +
          "2. Run application by running api.py script.\n" +
          "\n" +
          "\n" +
          "## API endpoints\n" +
          "* /api/rates/usd/{date} - get exchange rate USD to PLN for one day\n" +
          "* /api/rates/usd/{start_date}/{end_date} - get exchange rate USD to PLN for period of days\n" +
          "* /api/sales/{date} - get store sales sum for one day in USD and PLN\n" +
          "* /api/sales/{start_date}/{end_date} - get store sales sum for period of days in USD and PLN\n" +
          "\n" +
          "## Returned data structure\n" +
          "### For exchange rates\n" +
          "Here for /api/rates/usd/2003-1-1/2003-01-04\n" +
          "```json\n" +
          "[\n" +
          "{\n" +
          "\"date\": \"2003-01-01\",\n" +
          "\"interpolated\": 1,\n" +
          "\"rate\": 3.84\n" +
          "},\n" +
          "{\n" +
          "\"date\": \"2003-01-02\",\n" +
          "\"interpolated\": 0,\n" +
          "\"rate\": 3.83\n" +
          "},\n" +
          "{\n" +
          "\"date\": \"2003-01-03\",\n" +
          "\"interpolated\": 0,\n" +
          "\"rate\": 3.84\n" +
          "},\n" +
          "{\n" +
          "\"date\": \"2003-01-04\",\n" +
          "\"interpolated\": 1,\n" +
          "\"rate\": 3.84\n" +
          "}\n" +
          "]\n" +
          "```\n" +
          "Interpolated 1 means that that day was for example weekend and banks didn't work. This value is a copy from last known non interpolated value.\n" +
          "\n" +
          "### For sales\n" +
          "Here for /api/sales/2003-05-07\n" +
          "```json\n" +
          "{\n" +
          "\"converted_pln\": 63294.78,\n" +
          "\"date\": \"2003-05-07\",\n" +
          "\"original_usd\": 16700.47\n" +
          "}\n" +
          "```\n" +
          "\n" +
          "##Limitations\n" +
          "* API has limit for querying. For one IP you can make one request per second but max 30 requests per hour.\n" +
          "\n" +
          "## Others\n" +
          "* This API uses cache. That means when you refresh the page you get data from browser cache. The default timeout for cache is set to 60 seconds.\n" +
          "* The exchange rates are from NBP API: http://api.nbp.pl"
    }
  }
}</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.main-page {
  width: 100%;
  display: flex;
  justify-content: flex-start;
}

.container {
  width: 100%;


  .welcome-text{
    font-weight: bold;
    font-size: 32px;
    width: 100%;
    text-align: center;
    margin-bottom: 30px;
  }

  .description{
    padding: 20px 0;
    font-size: 18px;
    a{
      color: #5287ff;
      text-decoration: none;
    }

  }

  .readme{
    background-color: #cfcfcf;
    padding: 30px;
  }
}
</style>
