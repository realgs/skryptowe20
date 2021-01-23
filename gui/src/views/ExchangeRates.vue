<template>
  <div class="exchangerates">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <ExchangeRates msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import ExchangeRates from '@/components/ExchangeRates.vue'

export default {
  name: 'Home',
  components: {
    ExchangeRates
  }
}
</script>
