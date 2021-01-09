<template>
<v-menu
      ref="menu"
      v-model="menu"
      :close-on-content-click="false"
      transition="scale-transition"
      offset-y
      min-width="auto"
    >
      <template v-slot:activator="{ on }">
        <v-text-field
          v-model="date"
          label="Choose date"
          prepend-icon="mdi-calendar"
          readonly
          v-on="on"
        ></v-text-field>
      </template>
      <v-date-picker
        v-model="date"
        max="2005-12-31"
        min="2004-01-01"
      ></v-date-picker>
    </v-menu>
</template>
<script>
export default {
    name: "DatePicker",
    data: () => ({
    date: null,
    menu: false,
    }),
    watch: {
        menu (val) {
        val && setTimeout(() => (this.$refs.picker.activePicker = 'YEAR'))
        },
    },
}
</script>