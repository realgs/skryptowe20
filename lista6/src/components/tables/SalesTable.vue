<template>
  <div>
    <div v-if="status===200">
      <table>
        <thead>
        <tr>
          <th v-for="key in response_keys" :key="key">{{ key }}</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="response_item in response" :key="response_item['OrderDate']">
          <td v-for="key in response_keys" :key="key">{{ response_item[key] }}</td>
        </tr>
        </tbody>
      </table>
    </div>
    <div v-else-if="status===400">
      ERROR 400 <br>
      INVALID REQUEST
    </div>
    <div v-else-if="status===404">
      ERROR 404 <br>
      NOT FOUND
    </div>
    <div v-else-if="status===416">
      ERROR 416 <br>
      INVALID DATE RANGE
    </div>
    <div v-else-if="status===429">
      ERROR 429 <br>
      TOO MANY REQUESTS
    </div>
  </div>

</template>

<script>

export default {
  name: 'Table',

  props: {
    response: Array,
    status: Number,
  },
  data() {
    return {
      response_keys: [],
    };
  },
  mounted() {
    if (this.status === 200) {
      this.response_keys = Object.keys(this.response[0]);
    }
  },
};
</script>

<style scoped>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
  padding: 5px;
  margin: auto;
}
</style>
