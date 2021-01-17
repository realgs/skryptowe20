<template>
  <div>
    <div class="res" v-if="status===200">
      <RockerSwitch :value=true labelOn="TAB" labelOff="JSON"
                    size="small" backgroundColorOn="#088654" backgroundColorOff="#e3a405"
                    v-on:change="changeMode"/>

      <table v-if="tabMode">
        <thead>
        <tr>
          <th v-for="key in resKeys" :key="key">{{ key }}</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="resItem in res" :key="resItem['dateStr']">
          <td v-for="key in resKeys" :key="key">{{ resItem[key] }}</td>
        </tr>
        </tbody>
      </table>
      <pre v-else>
        <code>
{{ res }}
        </code>
      </pre>
    </div>
    <div v-else-if="status===400">
      ERROR 400 <br>
      BAD REQUEST
    </div>
    <div v-else-if="status===404">
      ERROR 404 <br>
      NOT FOUND
    </div>
    <div v-else-if="status===429">
      ERROR 429 <br>
      TOO MANY REQUESTS
    </div>
  </div>
</template>

<script>
import RockerSwitch from 'vue-rocker-switch';
import 'vue-rocker-switch/dist/vue-rocker-switch.css';

export default {
  name: 'Result',
  components: {
    RockerSwitch,
  },
  props: {
    res: Array,
    status: Number,
  },
  data() {
    return {
      resKeys: [],
      tabMode: true,
    };
  },
  methods: {
    changeMode(event) {
      this.tabMode = event;
    },
  },
  mounted() {
    if (this.status === 200) {
      this.resKeys = Object.keys(this.res[0]);
      this.resKeys.splice(0, 1);
      this.resKeys.splice(this.resKeys.indexOf('date'), 1);
    }
  },
};
</script>

<style lang="scss" scoped>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
  padding: 5px;
  margin: auto;
}

pre {
  text-align: left;
  width: fit-content;
  margin: auto;
}

.res {
  margin: 1rem;
}
</style>
