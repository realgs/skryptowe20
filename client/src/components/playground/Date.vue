<template>
  <div class="dateRange">
    <div>
      <label :for="minDate">Date range</label>
      <input type="checkbox" :id="minDate" v-model="isDateRange">
    </div>
    <DatePicker v-model="range" is-range v-if="isDateRange" :model-config="modelConfig"
                :masks="masks" :min-date="minDate" :max-date="maxDate">
      <template v-slot="{ inputValue, inputEvents }">
        <div class="flex justify-center items-center">
          <input
            :value="inputValue.start"
            v-on="inputEvents.start"
            class="border px-2 py-1 w-10 rounded focus:outline-none focus:border-indigo-300"
          />
          <svg
            class="w-1 h-1 mx-2"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M14 5l7 7m0 0l-7 7m7-7H3"
            />
          </svg>
          <input
            :value="inputValue.end"
            v-on="inputEvents.end"
            class="border px-2 py-1 w-10 rounded focus:outline-none focus:border-indigo-300"
          />
        </div>
      </template>
    </DatePicker>
    <DatePicker v-model="date" v-else :masks="masks" :model-config="modelConfig"
                :min-date="minDate" :max-date="maxDate">
      <template v-slot="{ inputValue, inputEvents }">
        <input
          class="bg-white border px-2 py-1 rounded w-10"
          :value="inputValue"
          v-on="inputEvents"
        />
      </template>
    </DatePicker>
  </div>
</template>

<script>
import DatePicker from 'v-calendar/lib/components/date-picker.umd';

export default {
  name: 'Date',
  components: {
    DatePicker,
  },
  props: {
    minDate: Date,
    maxDate: Date,
  },
  data() {
    return {
      modelConfig: {
        type: 'string',
        mask: 'YYYY-MM-DD',
      },
      masks: {
        input: 'YYYY-MM-DD',
      },
      range: {
        start: '2017-05-05',
        end: '2017-06-05',
      },
      date: '2017-05-05',
      isDateRange: false,
    };
  },
  watch: {
    range(newRange) {
      this.$emit('change', {
        range: newRange,
        date: this.date,
        isDateRange: this.isDateRange,
      });
    },
    date(newDate) {
      this.$emit('change', {
        range: this.range,
        date: newDate,
        isDateRange: this.isDateRange,
      });
    },
    isDateRange(newIsDateRange) {
      this.$emit('change', {
        range: this.range,
        date: this.date,
        isDateRange: newIsDateRange,
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.w-1 {
  width: 1rem;
}

.h-1 {
  height: 1rem;
}

.flex {
  display: flex;
  flex-wrap: wrap;
}

.justify-center {
  justify-content: center;
}

.dateRange {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
}

.w-10 {
  width: 10ch;
}

.border {
  border-radius: 0.3rem;
  border: solid gray 0.1rem;
}
</style>
