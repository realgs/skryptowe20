<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <v-img
          alt="Vuetify Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="100"
          src="./assets/app_logo.png"
          width="100"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/Silkypaladin/skryptowe20/tree/L5"
        target="_blank"
        text
      >
        <span class="mr-2">Latest Version</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
      <template v-slot:extension>
        <v-tabs v-model="tab" align-with-title>
          <v-tabs-slider color="yellow"></v-tabs-slider>
          <v-tab>Docs</v-tab>
          <v-tab>Request form</v-tab>
        </v-tabs>
      </template>
    </v-app-bar>

    <v-main>
        <v-tabs-items v-model="tab">
      <v-tab-item><Docs/></v-tab-item>
      <v-tab-item><RequestForm/></v-tab-item>
    </v-tabs-items>
      

    </v-main>
  </v-app>
</template>

<script>
import RequestForm from "./components/RequestForm";
import Docs from "./components/Docs"

export default {
  name: "App",

  components: {
    RequestForm,
    Docs
  },

  data () {
      return {
        tab: null,
      }
    },
};
</script>
