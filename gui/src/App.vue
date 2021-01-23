<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/exchangerates">Kursy wymiany</router-link> |
      <router-link to="/transactions">Wartości transakcji</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #4a6c8f;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #405c77;
}

#nav a.router-link-exact-active {
  color: #0242f0;
}
</style>
