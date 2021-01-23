<template>
  <div class="transactions">
    <Transactions msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
import Transactions from '@/components/Transactions.vue'

export default {
  name: 'Home',
  components: {
    Transactions
  }
}
</script>
