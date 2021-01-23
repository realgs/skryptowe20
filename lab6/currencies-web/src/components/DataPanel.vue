<template>
  <div class="currencies">
    <div class="currencies-menu">
      <div class="item" @click="openExchangeRates" :class="selectedExchangeRateSection ? 'selected' : '' ">
        USD - PLN
      </div>
      <div class="item" @click="openSalesData" :class="!selectedExchangeRateSection ? 'selected' : '' ">
        Sales data
      </div>
    </div>
    <div class="currencies-content-top">
      <div class="left-side-top">
        <div class="top">
          <p>Choose date range</p>
          <v-date-picker v-model="range" is-range color="orange" is-dark/>
          <div class="date-preview">
            <p>Selected start date: {{ getNormalDate(range.start) }}</p>
            <p>Selected end date: {{ getNormalDate(range.end) }}</p>
          </div>
        </div>
        <div class="middle" v-if="!selectedExchangeRateSection">
          <div class="currency-choose">
            <div class="item" @click="chooseUSD" :class="selectedUSD ? 'selected' : '' ">
              USD
            </div>
            <div class="item" @click="choosePLN" :class="!selectedUSD ? 'selected' : '' ">
              PLN
            </div>
          </div>
        </div>
        <div class="bottom">
          <div class="show-data" @click="showData">
            Show data
          </div>
          <div class="error-message" ref="errorShowDataMessage">
            {{ errorMessage }}
          </div>
        </div>
      </div>
      <div class="right-side-top">
        <div v-if="exchangeRatesList.length > 0 || (salesList.length > 0 && showSalesChart)">
          <line-chart :chart-data="dataForChart"/>
        </div>
      </div>

    </div>

    <div class="content-bottom" ref="contentBottomBoxExchange" v-show="selectedExchangeRateSection && exchangeRatesList.length > 0">
      <div v-for="exchangeRate in exchangeRatesList" :key="exchangeRate.date" class="item">
        <div>
          <span>Date: </span> {{ exchangeRate.date }}
        </div>
        <div>
          <span>PLN price for 1 USD: </span>{{ exchangeRate.rate }}
        </div>
        <div>
          <span>Value interpolated: </span>{{ exchangeRate.interpolated === 1 ? 'true' : 'false' }}
        </div>
      </div>
    </div>
    <div class="content-bottom" ref="contentBottomBoxSales" v-show="!selectedExchangeRateSection && salesList.length > 0">
      <div v-for="sale in salesList" :key="sale.date" class="item">
        <div>
          <span>Date: </span> {{ sale.date }}
        </div>
        <div>
          <span>Sale in PLN: </span>{{ sale.converted_pln }}
        </div>
        <div>
          <span>Sale in USD: </span>{{ sale.original_usd }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LineChart from "@/components/LineChart";

export default {
  name: "Teams",
  components: {
    LineChart
  },
  data() {
    return {
      range: {
        start: new Date(2003, 0, 1),
        end: new Date(2003, 0, 24)
      },
      dataForChart: null,
      showSalesChart: false
    }
  },
  computed: {
    selectedExchangeRateSection() {
      return this.$store.state.dataPanel.selectedExchangeRateSection
    },
    exchangeRatesList() {
      return this.$store.state.dataPanel.exchangeRatesList
    },
    salesList() {
      return this.$store.state.dataPanel.salesList
    },
    errorMessageHasChanged() {
      return this.$store.state.dataPanel.errorMessageHasChanged
    },
    errorMessage() {
      return this.$store.state.dataPanel.errorMessage
    },
    exchangeRatesListOnlyRates() {
      return this.exchangeRatesList.map((el) => {
        return el.rate
      })
    },
    exchangeRatesListOnlyDates() {
      return this.exchangeRatesList.map((el) => {
        return el.date
      })
    },
    salesListOnlyUSD() {
      return this.salesList.map((el) => {
        return el.original_usd
      })
    },
    salesListOnlyPLN() {
      return this.salesList.map((el) => {
        return el.converted_pln
      })
    },
    salesListOnlyDates() {
      return this.salesList.map((el) => {
        return el.date
      })
    },
    selectedUSD() {
      return this.$store.state.dataPanel.selectedUSD
    }
  },
  methods: {
    openExchangeRates() {
      this.$store.commit('dataPanel/setSelectedExchangeRateSection', true)
      this.$store.commit('dataPanel/setSalesList', [])
    },
    openSalesData() {
      this.$store.commit('dataPanel/setSelectedExchangeRateSection', false)
      this.$store.commit('dataPanel/setExchangeRatesList', [])
    },
    getNormalDate(date) {
      return date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate();
    },
    showData() {
      if (this.checkIfSelectedDateIsCorrect()) {
        if (this.selectedExchangeRateSection) {
          this.$store.dispatch('dataPanel/loadExchangeRates', {
            start: this.getNormalDate(this.range.start),
            end: this.getNormalDate(this.range.end)
          })
        } else {
          this.$store.dispatch('dataPanel/loadSalesData', {
            start: this.getNormalDate(this.range.start),
            end: this.getNormalDate(this.range.end)
          })
        }
      }
    },
    checkIfSelectedDateIsCorrect() {
      let today = new Date()
      if (this.range.start.getTime() > today.getTime() || this.range.end.getTime() > today.getTime()) {
        this.$store.commit('dataPanel/setErrorMessage', "You have exceeded current date!")
        return false;
      }
      return true;
    },
    fillDataForExchangeRatesChart() {
      this.dataForChart = {
        labels: this.exchangeRatesListOnlyDates,
        title: 'PLN price for one USD',
        datasets: [
          {
            pointBackgroundColor: '#1f77f8',
            borderColor: '#777676',
            data: this.exchangeRatesListOnlyRates
          }
        ]
      }
    },
    fillDataForSalesChart() {
      this.dataForChart = {
        labels:  this.salesListOnlyDates,
        title: this.selectedUSD ? 'Sales in USD' : 'Sales in PLN',
        datasets: [
          {
            pointBackgroundColor: '#1f77f8',
            borderColor: '#777676',
            data: this.selectedUSD ? this.salesListOnlyUSD : this.salesListOnlyPLN
          }
        ]
      }
    },
    adjustContentBottomSize(itemsCount) {
      let contentBottomBox = null;
      if(this.selectedExchangeRateSection){
        contentBottomBox = this.$refs.contentBottomBoxExchange;
      }else{
        contentBottomBox = this.$refs.contentBottomBoxSales;
      }
      contentBottomBox.style.maxHeight = (36 * itemsCount) + 'px'

    },
    chooseUSD() {
      if(!this.selectedUSD){
        this.showSalesChart = false
        this.$store.commit('dataPanel/setSelectedUSD', true)
        this.fillDataForSalesChart()
        this.$nextTick(()=>{
          this.showSalesChart = true
        })
      }

    },
    choosePLN() {
      if(this.selectedUSD){
        this.showSalesChart = false
        this.$store.commit('dataPanel/setSelectedUSD', false)
        this.fillDataForSalesChart()
        this.$nextTick(()=>{
          this.showSalesChart = true
        })
      }

    }
  },
  watch: {
    errorMessageHasChanged() {
      if (this.errorMessageHasChanged) {
        let errMessageDiv = this.$refs.errorShowDataMessage;
        errMessageDiv.style.opacity = 1
        setTimeout(() => {
          this.$store.commit('dataPanel/setErrorMessageHasChanged', false)
          errMessageDiv.style.opacity = 0
        }, 5000)
      }
    },
    exchangeRatesList() {
      this.adjustContentBottomSize(this.exchangeRatesList.length)
      this.fillDataForExchangeRatesChart()
    },
    salesList() {
      this.adjustContentBottomSize(this.salesList.length)
      this.fillDataForSalesChart()
      this.showSalesChart = true
    }
  }
}
</script>

<style scoped lang="scss">
.currencies {
  width: 100%;

  .currencies-menu {
    width: 100%;
    height: 60px;
    display: flex;
    border: solid 2px var(--border-color-1);
    background-color: var(--bg-block-color);

    .item {
      flex: 1;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      font-size: 22px;
      transition: all ease-in-out .2s;

      &.selected {
        background-color: var(--bg-selected);
      }

      &:hover, &.selected {
        font-size: 24px;
      }
    }
  }


  .currencies-content-top {
    width: 100%;
    margin-top: 30px;
    border: solid 2px var(--border-color-1);
    background-color: var(--bg-block-color);
    height: 600px;
    display: flex;
    align-items: center;
    padding: 0 40px;

    .left-side-top {
      width: 300px;
      height: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-direction: column;

      .top {
        display: flex;
        flex-direction: column;
        align-items: center;

        .date-preview {
          width: 100%;
          display: flex;
          flex-direction: column;
          align-items: center;

          p {
            margin: 10px 0 0;
          }
        }
      }

      .middle {
        width: 50%;
        height: 30px;
        border: solid 2px var(--border-color-1);
        background-color: var(--bg-block-color);

        .currency-choose {
          display: flex;
          height: 100%;
          .item {
            flex: 1;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 16px;
            transition: all ease-in-out .2s;

            &.selected {
              background-color: var(--bg-selected);
            }

            &:hover, &.selected {
              font-size: 18px;
            }
          }
        }
      }

      .bottom {
        position: relative;
        padding-bottom: 80px;

        .show-data {
          font-weight: bold;
          font-size: 24px;
          padding: 10px 60px;
          cursor: pointer;
          border: solid 2px var(--border-color-1);
          transition: all ease-in-out .2s;

          &:hover {
            background-color: var(--bg-selected);
          }
        }

        .error-message {
          position: absolute;
          top: 60px;
          left: 0;
          right: 0;
          color: red;
          opacity: 0;
          transition: all ease-in-out .5s;
          text-align: center;
        }
      }
    }

    .right-side-top {
      position: relative;
      margin: 0 auto;
      padding: 0 1rem;
      padding-bottom: 1rem;
      height: auto;
      width: 100%;
      min-height: 400px;
    }
  }

  .content-bottom {
    width: 100%;
    margin-top: 5px;
    border: solid 2px var(--border-color-1);
    background-color: var(--bg-block-color);
    max-height: 0;
    display: flex;
    flex-direction: column;
    padding: 0 40px;
    transition: all ease-in-out .2s;

    .item {
      width: 100%;
      display: flex;
      border-bottom: solid 1px var(--border-color-1);

      &:last-child {
        border-bottom: none;
      }

      div {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 35px;

        span {
          color: #949494;
          margin-right: 20px;
        }
      }
    }
  }

  @media only screen and (max-width: 1000px) {
    .currencies{
      .currencies-content-top ,.content-bottom{
        padding: 0 5px;
      }
    }
  }
}
</style>