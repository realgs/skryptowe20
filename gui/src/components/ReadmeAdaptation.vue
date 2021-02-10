<template>
  <div class="hello">
    <h1>Projekt z języków skryptowych</h1>
    <h2>Wstęp</h2> <br>
    <p>
      API zostało oparte o framework FastAPI, natomiast front-end (a więc i ta strona) stworzony został przy użyciu Vue.js. <br>
      Jako zbiór danych wykorzystano zbiór <a href="https://github.com/huynhsamha/quick-mongo-atlas-datasets">Sample Supply Store Dataset</a>. <br>
      Korzystając z powyższych zakładek można w prosty sposób wyświetlić informacje o kursach wymiany USD na PLN oraz o transakcjach z powyższej bazy danych. <br>
      Można uzyskać informacje dla pojedynczego dnia, jak i dla zakresu dat. <br>
      Dane o kursach wymiany zostałe pobrane z <a href=http://api.nbp.pl/>NBP Web API</a>, uzupełnione o stawki interpolowane w przypadku dni, dla którego nie podano nowego kursu. <br>
    </p>
    
    <h2>Inne</h2> <br>
    <ul>
      <li> Dostępne są kursy wymiany dla dat z przedziału 01.01.2014 - 31.12.2015 </li>
      <li> Dostępne są wartości transakcji dla dat z przedziału 01.01.2014 - 31.12.2015 </li>
    </ul>
  </div>
</template>

<script>

export default {
  name: 'ReadmeAdaptation',
}

</script>

<style scoped>
h2 {
  margin: 10px 0 0;
}
p {
  margin: 0px 0 0;
}
ul {
  margin-top: 0;
  list-style-type: none;
  padding: 0;
}
li {
  margin: 0 10px;
}
a {
  color: #001aff;
}
 
</style>
