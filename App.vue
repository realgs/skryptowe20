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
  components: {

  }
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}

.menu {
  display: flex;
  align-items: center;
  justify-content: space-around;
}

.menu-item{
  flex: 1;
  text-align: center;
}

.menu-text{
  color: #373737;
  font-size: 21px;
  padding: 10px;
  border-bottom: 7px solid #eeeeee;
  width: fit-content;
}

.menu-text:hover {
  border-bottom: 7px solid #737373;
}

.routerlink {
  color: transparent;
}

.siteContent {
  background-color: #f3f3f3;
  margin: 20px;

}

</style>
