<template>
  <div class="main">
    <Rate/>
    <Sale/>
  </div>
</template>
<script>
import Rate from '@/components/playground/Rate.vue';
import Sale from '@/components/playground/Sale.vue';

export default {
  components: {
    Sale,
    Rate,
  },
};
</script>
