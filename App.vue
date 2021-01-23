<template>
  <div id="app">
    <div class="menu">
      <router-link to="/" class="routerlink">
        <div class="menu-item">
          <div class="menu-text">
            Home
          </div>
        </div>
      </router-link>
      <router-link to="/sale" class="routerlink">
        <div class="menu-item">
          <div class="menu-text">
            Sale on selected day
          </div>
        </div>
      </router-link>
      <router-link to="/sales" class="routerlink">
        <div class="menu-item">
          <div class="menu-text">
            Sales from date period
          </div>
        </div>
      </router-link>
      <router-link to="/rate" class="routerlink">
        <div class="menu-item">
          <div class="menu-text">
            Currency rate on selected day
          </div>
        </div>
      </router-link>
      <router-link to="/rates" class="routerlink">
        <div class="menu-item">
          <div class="menu-text">
            Currency rates from date period
          </div>
        </div>
      </router-link>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>


export default {
  name: 'App',
  components: {}
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #e7e7e7;
}

.menu {
  display: flex;
  align-items: center;
  justify-content: space-around;
}

.menu-item {
  flex: 1;
  text-align: center;
}

.menu-text {
  color: #f1f1f1;
  font-size: 21px;
  padding: 10px;
  border-bottom: 7px solid #5d5d5d;
  width: fit-content;
}

.menu-text:hover {
  border-bottom: 7px solid #f1f1f1;
}

.routerlink {
  color: transparent;
}

.siteContent {
  background-color: #f3f3f3;
  margin: 20px;
}

.searchButton {
  background-color: transparent;
  color: #e3e3e3;
  font-size: 20px;
  border: 2px solid #e7e7e7;
}

.searchButton:hover {
  background-color: #e3e3e3;
  color: #232323;
  border: 2px solid #e7e7e7;
  cursor: pointer;
}

.searchButton:focus {
  outline: 0;
}

.tableWithFixHead {
  overflow-y: auto;
  overflow-x: hidden;
  height: 400px;
  width: 73%;
  margin: auto;
}

.dataTable {
  background-color: #232323;
  table-layout: fixed;
  width: 100%;
  border: 0;
  border-collapse: collapse;
}

tr td {
  padding: 3%;
  width: 27%;
  display: inline-block;
}

tr th {
  padding: 3%;
  width: 27%;
  display: inline-block;
}

tr {
  width: 100%;
  display: inline-block;
}

tr:hover {
  background-color: #3b3b3b;
}

select {
  background: #232323;
  font-size: 21px;
  color: #e7e7e7;
  border: 2px solid #e7e7e7;
  cursor: pointer;
}

select:focus {
  outline: 0;
}

input[type="date"] {
  background: #232323;
  font-size: 18px;
  color: #e7e7e7;
  border: 2px solid;
}

input[type="date"]:focus {
  outline: 0;
}

input[type="date"]::-webkit-calendar-picker-indicator {
  background-color: #e7e7e7;
}

</style>
