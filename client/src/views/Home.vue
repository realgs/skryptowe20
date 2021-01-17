<template>
  <div class="home">
    <h1>
      Currency exchange and sales api
    </h1>
    <h2>
      Some explanations and rules
    </h2>
    {code} - three letter currency code <br>
    {date},{startDate},{endDate} - date in format: "yyyy-mm-dd"<br><br>

    There are per-person query limits:<br>
    1 per second<br>
    50 per hour<br>
    200 per day<br>

    <h2>
      Routes
    </h2>
    <div class="route">
      <route url="/rates/{code}/{date}"
             result="Returns the exchange rate for the {code} currency on {date}<br>
             Returns 400_BAD_REQUEST when {date} format is incorrect<br>
             Returns 404_NOT_FOUND when there is no exchange rate with and date={date}
             in the database"
      />
      <example url="/rates" :inputs="['code', 'date']"/>
    </div>

    <div class="route">
      <route url="/rates/{code}/{startDate}/{endDate}"
             result="Returns the exchange rates for the {Code} currency between {startDate} and
             {endDate}<br>Returns 400_BAD_REQUEST when {startDate} or {endDate} format is incorrect
             or when {startDate} is after {endDate}<br>Returns 404_NOT_FOUND when there is no
             exchange rate with code={code} and date between {startDate} and {endDate}<br><br>
             Results are cached for 10 minutes<br>"/>
      <example url="/rates" :inputs="['code', 'startDate', 'endDate']"/>
    </div>

    <div class="route">
      <route url="/sales/{date}"
             result="Returns the sales result on {date}<br>Returns 400_BAD_REQUEST when {date}
             format is incorrect<br>Returns 404_NOT_FOUND when there is no sale result with
             date={date} in the database<br>"/>
      <example url="/sales" :inputs="['date']"/>
    </div>

    <div class="route">
      <route url="/sales/{startDate}/{endDate}"
             result="Returns the sales results between {startDate} and {endDate}<br>
             Returns 400_BAD_REQUEST when {startDate} or {endDate} format is incorrect or when
             {startDate} is after {endDate}<br>Returns 404_NOT_FOUND when there is no sale result
             with date between {startDate} and {endDate}<br><br>Results are cached for 10 minutes
             <br>"/>
      <example url="/sales" :inputs="[ 'startDate', 'endDate']"/>
    </div>
  </div>
</template>

<script>
import Route from '@/components/home/Route.vue';
import Example from '@/components/home/Example.vue';

export default {
  name: 'Home',
  components: {
    Example,
    Route,
  },
};
</script>

<style lang="scss" scoped>
h1 {
  margin: 0;
}

.route {
  background-color: white;
  margin: 20px auto;
  border-radius: 10px;
  box-shadow: 3px 3px 10px gray;
  width: 80%;
  max-width: 1200px;
  padding: 10px 30px;
}

@media all and (min-width: 820px) {
  .route {
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: center;
    align-content: space-between;
  }
}
</style>
