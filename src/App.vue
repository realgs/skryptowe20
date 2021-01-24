<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="100"
          src="./assets/nbp_api.png"
          width="100"
        />
      </div>
      <v-btn href="./" target="_blank" text>
        <span class="mr-2">API</span>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <div class="text-h1 pa-4 mb-4" align="center">
          NBP Sales and Rates API
        </div>
        <v-row justify="center" no-gutters>
          <v-col cols="6" sm="6">
            <v-card color="grey" outlined dark tile>
              <v-card-text>
                <p class="display-1 bold">Descriptions</p>
              </v-card-text>
            </v-card>
            <v-card
              v-for="point in endpoints"
              :key="point.desc"
              :color="point.color"
              class="pa-2"
              outlined
              tile
            >
              {{ point.desc }}
            </v-card>
          </v-col>
          <v-col cols="12" sm="6">
            <v-card color="grey" outlined dark tile>
              <v-card-text>
                <p class="display-1 bold">API URLS</p>
              </v-card-text>
            </v-card>
            <v-card
              v-for="point in endpoints"
              :key="point.desc"
              class="pa-2"
              :color="point.color"
              outlined
              tile
            >
              {{ point.url }}
            </v-card>
          </v-col>
        </v-row>

        <v-row class="mt-2">
          <v-col>
            <v-tabs v-model="tab" background-color="transparent" fixed-tabs>
              <v-tabs-slider color="cyan"></v-tabs-slider>
              <v-tab v-for="tab in tabs" :key="tab.subpage">
                {{ tab.subpage }}
              </v-tab>
            </v-tabs>

            <v-tabs-items v-model="tab">
              <v-tab-item v-for="tab in tabs" :key="tab.subpage">
                <component
                  class="mp-6"
                  :is="tab.content"
                  v-bind:url="tab.url"
                ></component>
              </v-tab-item>
            </v-tabs-items>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
    <v-footer dark padless>
      <v-card flat tile class="primary white--text text-center flex">
        <v-card-text>
          <v-btn
            v-for="icon in icons"
            :key="icon"
            class="mx-4 white--text"
            icon
          >
            <v-icon size="24px">
              {{ icon }}
            </v-icon>
          </v-btn>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-text class="white--text">
          {{ new Date().getFullYear() }} — <strong>@ptrswr</strong>
        </v-card-text>
      </v-card>
    </v-footer>
  </v-app>
</template>

<script>
import DataDaily from "./components/DataDaily";
import DataRange from "./components/DataRange";
import axios from "axios";
import Chart from "./components/Chart";
export default {
  name: "App",
  components: {
    DataDaily,
    DataRange,
  },
  data: () => ({
    icons: ["mdi-facebook", "mdi-twitter", "mdi-linkedin", "mdi-instagram"],
    tab: null,
    tabs: [
      { subpage: "Rates Daily", content: DataDaily, url: "rates" },
      { subpage: "Rates Range", content: DataRange, url: "rates" },
      { subpage: "Sales Daily", content: DataDaily, url: "sales" },
      { subpage: "Sales Range", content: DataRange, url: "sales" },
    ],
    endpoints: [
      {
        desc: "Get USD rates from  specified day",
        url: "http://127.0.0.1:5000/rates/{date}",
        color: "transparent",
      },
      {
        desc: "Get USD rates from specified date range",
        url: "http://127.0.0.1:5000/rates/{start_date}/{end_date}",
        color: "grey lighten-2",
      },
      {
        desc: "Get sales values in USD and PLN from specified day",
        url: "http://127.0.0.1:5000/sales/{date}",
        color: "transparent",
      },
      {
        desc: "Get sales values in USD and PLN from specified date range",
        url: "http://127.0.0.1:5000/sales/{start_date}/{end_date}",
        color: "grey lighten-2",
      },
    ],
  }),
};
</script>
