<template>
  <div id="app">
    <nav id="nav">
      <router-link to="/">Home</router-link>
      |
      <router-link to="/playground">Playground</router-link>
    </nav>
    <router-view/>
  </div>
</template>

<style lang="scss" scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 3px 3px 10px gray;
  box-sizing: border-box;
  width: fit-content;
  margin: 10px auto;
  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>

<style lang="scss">
root {
  margin: 0;
}

body {
  background-color: #dfffea;
  margin: 0;
}
</style>
