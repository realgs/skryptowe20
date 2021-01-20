<template>
  <div class="home">
    <NavBar />
    <ApiDescription />
  </div>
</template>

<script>
import ApiDescription from "@/components/ApiDescription.vue";
import NavBar from "@/components/NavBar.vue";

export default {
  name: "Home",
  components: {
    NavBar,
    ApiDescription,
  },
};
</script>
