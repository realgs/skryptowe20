<template>
  <v-toolbar color="blue darken-4" dark>
    <v-toolbar-title>{{ appTitle }}</v-toolbar-title>
  </v-toolbar>
</template>

<script>
export default {
  name: "AppNavigation",
  data() {
    return {
      appTitle: "Api app"
    };
  }
};
</script>

<style scoped></style>
