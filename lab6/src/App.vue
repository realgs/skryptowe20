<template>
  <v-app>
    <app-navigation></app-navigation>

    <v-main>
      <instructionDisplay />
      <SettingsDisplay />
    </v-main>
  </v-app>
</template>

<script>
import instructionDisplay from "./components/instructionDisplay";
import AppNavigation from "./components/AppNavigation";
import SettingsDisplay from "./components/settingsDisplay";

export default {
  name: "App",

  components: {
    instructionDisplay,
    SettingsDisplay,
    AppNavigation
  },

  data: () => ({
    //
  })
};
</script>
