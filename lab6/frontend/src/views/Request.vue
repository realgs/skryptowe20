<template>
  <div class="request">
    <NavBar />
    <Input />
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import Input from "@/components/Input.vue";

export default {
  name: "Request",
  components: {
    NavBar,
    Input,
  },
};
</script>
