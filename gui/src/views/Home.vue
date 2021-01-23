<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <ReadmeAdaptation msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import ReadmeAdaptation from '@/components/ReadmeAdaptation.vue'

export default {
  name: 'Home',
  components: {
    ReadmeAdaptation
  }
}
</script>
