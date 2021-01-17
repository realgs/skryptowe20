<template>
  <div>
    <h3 class="topic">
      {{ url }}
    </h3>
    <div class="result" v-html="result">
    </div>
  </div>
</template>

<script>
export default {
  name: 'Route',
  props: {
    url: String,
    result: String,
  },
};
</script>

<style lang="scss">
</style>
