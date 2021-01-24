<template>
  <div>
    <header>
      <h1>USD currency rates and product sales API</h1>
    </header>

    <Form/>

    <h3>Limits</h3>
    <p class="desc">There is a limit put on every kind (sales/exchange) of request from one ip address equal to
      <strong>50 requests per minute</strong>.</p>
    <p class="desc">There is also a limit put on the sum of all requests and it is equal to <strong>400 requests per
      minute</strong>.</p>
    <p class="desc">The answer on exceeding the limit is the error code <strong>429</strong>.</p>

    <h3>Cache</h3>
    <p class="desc">Cache mechanism checks, if the request has been made earlier.
      If so - it sends the remembered value. If not - it remembers the answer.</p>
    <p class="desc">Cache refreshes in every <strong>24 hours</strong>.</p>

  </div>
</template>

<script>
import Form from "@/components/Form";

export default {
  name: 'Main',
  components: {
    Form
  },
  data() {
    return {}
  },
  computed: {}
}
</script>


<style scoped>
h3 {
  margin: 40px 0 0;
  text-align: center;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

.desc {
  text-align: left;
}

</style>
