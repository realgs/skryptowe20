<template>
  <div class="header">
    <img src="../assets/logo-currencies.jpg" class="logo" @click="openMainPage"/>
    <div class="header-buttons">
      <div  @click="openCurrencies" :class="currenciesSelected ? 'selected' : '' ">
        Data panel
      </div>
      <div  @click="openContact" :class="salesSelected ? 'selected' : '' ">
        Contact
      </div>
    </div>
  </div>

</template>

<script>
export default {
  name: "Header",
  computed: {
    currenciesSelected() {
      return this.$route.name === 'DataPanel'
    },
    salesSelected() {
      return this.$route.name === 'Contact'
    }

  },
  methods: {
    openCurrencies() {
      this.$router.push('data-panel')
    },
    openContact() {
      this.$router.push('contact')
    },
    openMainPage(){
      this.$router.push('/')

    }
  }
}
</script>

<style scoped lang="scss">
.header {
  width: 100%;
  height: 80px;
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px 0;
  justify-content: space-between;
  background-color: #161b22;
  color: white;

  .logo {
    height: 100%;
    margin-left: 50px;
    border-radius: 10px;
    cursor: pointer;
  }

  .header-buttons {
    display: flex;
    height: 100%;
    align-items: center;
    margin-right: 50px;

    div {
      display: flex;
      padding: 0 20px;
      align-items: center;
      justify-content: center;
      height: 50%;
      margin-left: 20px;
      font-size: 20px;
      cursor: pointer;
      transition: all ease-in-out .2s;
      border-radius: 5px;

      &:hover, &.selected {
        background-color: #727272;
      }

    }
  }

}
</style>