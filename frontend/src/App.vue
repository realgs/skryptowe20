<template>
  <v-app>
    <v-app-bar
      app
      color="#FFD369"
      flat
    >
      <v-container class="py-0 fill-height">
        <v-img
          alt="Chart Logo"
          class="shrink mr-2"
          contain
          src="./assets/chart-icon.png"
          transition="scale-transition"
          width="40"
        />
        <v-img
          alt="App Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="300"
          src="./assets/logo.png"
        />
        <v-spacer></v-spacer>
      </v-container>
      <v-btn
        href="https://github.com/joannasroka/skryptowe20/tree/L6"
        target="_blank"
        text
      >
        <v-img
          alt="Github Logo"
          class="shrink mr-2"
          contain
          src="./assets/github.png"
          transition="scale-transition"
          width="30"
        />
        <span class="mr-2">Github</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
      <template v-slot:extension>
        <v-tabs v-model="tab" align-with-title>
          <v-tabs-slider color="yellow"></v-tabs-slider>
          <v-tab>Home</v-tab>
          <v-tab>Exchange rates</v-tab>
          <v-tab>Sales</v-tab>
        </v-tabs>
      </template>
    </v-app-bar>
    <v-main>
      <v-tabs-items v-model="tab">
        <v-tab-item>
          <Home/>
        </v-tab-item>
        <v-tab-item>
          <ExchangeRates/>
        </v-tab-item>
        <v-tab-item>
          <Sales/>
        </v-tab-item>
      </v-tabs-items>
    </v-main>
  </v-app>
</template>
<script>
import ExchangeRates from '@/views/ExchangeRates.vue';
import Sales from '@/views/Sales.vue';
import Home from '@/views/Home.vue';

export default {
  name: 'App',
  components: {
    Home,
    Sales,
    ExchangeRates,
  },

  data() {
    return {
      tab: null,
    };
  },
};
</script>
