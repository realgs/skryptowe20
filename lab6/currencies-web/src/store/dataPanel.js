import axios from "axios";
import {axiosBaseUrl} from '@/config/variables'

export default {
    namespaced: true,
    state: {
        selectedExchangeRateSection: true,
        exchangeRatesList: [],
        salesList: [],
        errorMessage: 'error',
        errorMessageHasChanged: false,
        selectedUSD: true,
        dataForChart: {},
        showSalesChart: false
    },
    mutations: {
        setSelectedExchangeRateSection(state, payload) {
            state.selectedExchangeRateSection = payload
        },
        setExchangeRatesList(state, payload) {
            state.exchangeRatesList = payload
        },
        setSalesList(state, payload) {
            state.salesList = payload
        },
        setErrorMessage(state, payload) {
            state.errorMessage = payload
            state.errorMessageHasChanged = true
        },
        setErrorMessageHasChanged(state, payload) {
            state.errorMessageHasChanged = payload
        },
        setSelectedUSD(state, payload){
            state.selectedUSD = payload
        },
        setDataForChart(state, payload){
            state.dataForChart = payload
        },
        setShowSalesChart(state, payload){
            state.showSalesChart = payload
        }
    },
    actions: {
        loadExchangeRates({commit}, data) {
            axios.defaults.baseURL = axiosBaseUrl;
            axios.get('/api/rates/usd/' + data.start + '/' + data.end)
                .then(response => {
                    if (!response.data.message) {
                        commit('setExchangeRatesList', response.data)
                    } else {
                        commit('setErrorMessage', response.data.message)
                    }
                })
        },
        loadSalesData({commit}, data) {
            axios.defaults.baseURL = axiosBaseUrl;
            axios.get('/api/sales/' + data.start + '/' + data.end)
                .then(response => {
                    if (!response.data.message) {
                        commit('setSalesList', response.data)
                    } else {
                        commit('setErrorMessage', response.data.message)
                    }
                })
        }
    }
}