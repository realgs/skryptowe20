<template>
  <div>
    <h3 class="request">
      <div class="inputs">
        {{ url }}
        <div v-for="input in inputs" :key="input">
          /<label>
          <input :class="input" v-model="inputsData[input]" :placeholder="input"
                 :maxlength="input==='code' ? 3 : 10">
        </label>
        </div>
      </div>
      <button v-on:click="sendRequest">SEND</button>
    </h3>
    <Result :res="response" :status="status" :key="requestURL"/>
  </div>
</template>

<script>
import axios from 'axios';
import config from '@/config';
import Result from '@/components/result/Result.vue';

export default {
  name: 'Example',
  components: {
    Result,
  },
  props: {
    url: String,
    inputs: Array,
  },
  data() {
    return {
      requestURL: '',
      response: [],
      status: 0,
      inputsData: {},
    };
  },
  methods: {
    sendRequest() {
      let requestURL = config.apiPath.concat(this.url);
      for (let i = 0; i < this.inputs.length; i += 1) {
        requestURL += `/${this.inputsData[this.inputs[i]]}`;
      }
      axios.get(requestURL)
        .then((response) => {
          this.response = response.data;
          this.status = 200;
        })
        .catch((error) => {
          this.status = error.response.status;
        })
        .finally(() => {
          this.requestURL = requestURL;
        });
    },
  },
};
</script>

<style lang="scss" scoped>

.inputs {
  display: flex;
}

.code {
  width: 4ch;
}

.date, .startDate, .endDate {
  width: 10ch;
}

.request {
  display: flex;
  align-items: center;
  flex-direction: column;
}

.result {
  text-align: left;
}

pre {
  margin: auto;
  width: fit-content;
}

@media all and (min-width: 900px) {
  .request {
    flex-direction: row;
    justify-content: center;
  }
}
</style>
