<template>
  <div class="page">
    <Header/>
    <div class="page-wrapper" :style="cssVars">
      <router-view/>
    </div>
  </div>
</template>

<script>

import Header from "@/components/Header";


export default {
  name: 'App',
  components: {Header},
  computed: {
    cssVars() {
      return {
        '--bg-block-color': '#131822',
        '--bg-block-hover': '#1e2435',
        '--border-color-1': '#30363d',
        '--border-color-2': '#777676',
        '--bg-selected': '#25315b',
      }
    }
  }

}
</script>


<style lang="scss">
@font-face {
  font-family: Roboto;
  src: url('./fonts/Roboto-Regular.ttf');
  font-style: normal;
  font-weight: normal;
}

@font-face {
  font-family: Roboto;
  src: url('./fonts/Roboto-Bold.ttf');
  font-style: normal;
  font-weight: bold;
}

@font-face {
  font-family: Roboto;
  src: url('./fonts/Roboto-Bold.ttf');
  font-style: normal;
  font-weight: 500;
}

@font-face {
  font-family: Roboto;
  src: url('./fonts/Roboto-Light.ttf');
  font-style: normal;
  font-weight: 300;
}

html, body, .page {
  width: 100%;
  margin: 0;
  padding: 0;
  font-family: Roboto, serif !important;
  font-weight: 400;
  font-size: 16px;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  color: white;
}

body {
  min-width: 320px;
  overflow-x: hidden;
}

html, body {
  width: 100%;
  height: 100%;
  background-color: #0d1117;
}

* {
  box-sizing: border-box;
}

b, strong, .bold {
  font-weight: bold;
}

.page-wrapper {
  width: 100%;
  padding: 30px 60px;
  padding-top: 15px;
}

@media only screen and (max-width: 1000px) {
  .page {
    .page-wrapper {
      width: 100%;
      padding: 10px 3px;
    }
  }
}
</style>
