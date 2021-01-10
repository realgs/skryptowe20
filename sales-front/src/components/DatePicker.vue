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
          :label="label"
          prepend-icon="mdi-calendar"
          readonly
          v-on="on"
          required
          :rules="rules"
        ></v-text-field>
      </template>
      <v-date-picker
        ref="picker"
        v-model="date"
        max="2005-12-31"
        min="2004-01-01"
        @change="$emit('setDate', date)"
      ></v-date-picker>
    </v-menu>
</template>
<script>
export default {
    name: "DatePicker",
    props: ['label', 'rules'],
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