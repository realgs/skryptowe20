<template>
    <div>
        <div>
            <h1>Choose the type of your request</h1>
            <b-button-group vertical>
                <b-button class="mb-3" @click="onRates()" :class="{ 'btn-success': request == 'rates' }">
                    USD/PLN Exchange rate request
                </b-button>
                <b-button class="mb-3" @click="onSales()" :class="{ 'btn-success': request == 'sales' }">
                    Sales request
                </b-button>
            </b-button-group>
        </div>
        <div v-if="request">
            <div>
                <h2>Choose the date range</h2>
                <b-form @submit="onSubmit">
                    <b-form-datepicker class="datepicker" v-model="form.start" placeholder="Choose starting date"
                                       locale="en" :min="minDate" :max="maxDate"
                                       value-as-date today-button></b-form-datepicker>
                    <b-form-datepicker class="datepicker" v-model="form.end" placeholder="Choose ending date"
                                       locale="en" :min="minDate" :max="maxDate"
                                       value-as-date today-button></b-form-datepicker>
                    <b-button class="submit-button" type="submit" variant="success">Send request</b-button>
                </b-form>
            </div>
            <b-alert variant="danger" :show="errors != null">
                <p v-for="(error, i) in errors" :key="i">{{ error }}</p>
            </b-alert>
        </div>
        <div>
            <RatesResultsData v-bind:resultsData="resultsData" v-if="request == 'rates'"/>
        </div>
        <div >
            <SalesResultsData v-bind:resultsData="resultsData" v-if="request == 'sales'"/>
        </div>

    </div>
</template>

<script>
    import RatesResultsData from "/src/components/RatesResultsData.vue";
    import SalesResultsData from "/src/components/SalesResultsData.vue";
    import moment from "moment";
    const dateFormat = "YYYY-MM-DD";
    export default {
        name: "Request",
        components: {
            RatesResultsData,
            SalesResultsData,
        },
        data() {
            return {
                request: null,
                minDate: null,
                maxDate: null,
                form: {
                    start: null,
                    end: null,
                },
                resultsData: null,
                errors: null,
            };
        },
        methods: {
            onRequest(requestType, min, max) {
                this.request = requestType;
                this.minDate = min;
                this.maxDate = max;
            },

            onRates() {
                this.onRequest("rates", new Date(2002, 0, 2), new Date());
            },

            onSales() {
                this.onRequest("sales", new Date(2012, 6, 4), new Date(2016, 1, 19));
            },

            onSubmit(event) {
                event.preventDefault();
                const errors = [];

                if (this.form.start == null)
                    errors.push("No starting date specified");

                if (this.form.end == null)
                    errors.push("No ending date specified");

                if (errors.length > 0) {
                    this.errors = errors;
                    return;
                }

                if (!this.rangeSatisfiable())
                    errors.push("Invalid range, starting date is later than ending date");

                if (!this.dateInRange(this.form.start))
                    errors.push("Starting date is out of the correct range");

                if (!this.dateInRange(this.form.end))
                    errors.push("Ending date is out of the correct range");

                if (errors.length > 0) {
                    this.errors = errors;
                    return;
                }

                const from = moment(this.form.start).format(dateFormat);
                const to = moment(this.form.end).format(dateFormat);

                var requestUrl;
                if (this.request == 'rates')
                    requestUrl = `/api/rates/USD/${from}/${to}`
                else if (this.request == 'sales')
                    requestUrl = `/api/sales/${from}/${to}`

                fetch(requestUrl)
                    .then((response) => response.json())
                    .then((data) => {
                        this.resultsData = data;
                        this.errors = null;
                    });
            },

            dateInRange(date) {
                return date <= this.maxDate && date >= this.minDate;
            },

            rangeSatisfiable() {
                return this.form.start <= this.form.end;
            },
        },
    };
</script>

<style scoped>
    h1 {
        margin: 20px 0 40px;
    }

    h2 {
        margin-top: 50px;
    }

    .datepicker {
        width: 304px;
        margin: 25px 0 20px 42%;
    }

    .submit-button {
        margin-top: 20px;
        margin-bottom: 50px;
    }
</style>
