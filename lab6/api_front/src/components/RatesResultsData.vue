<template>
    <div>
        <div class="rates-chart" v-if="resultsData">
            <canvas ref="ratesChart"></canvas>
        </div>
        <div>
            <b-table class="table" striped hover :items="resultsData" head-variant="dark" bordered
                     :fields="fields" outlined v-if="resultsData"></b-table>
        </div>
    </div>
</template>

<script>
    import Chart from "chart.js";
    export default {
        name: "RatesResultsData",
        props: ["resultsData"],
        data() {
            return {
                chart: null,
                fields: [
                    {
                        key: "date",
                        label: "Date",
                    },
                    {
                        key: "interpolated",
                        label: "Value interpolated",
                    },
                    {
                        key: "rate",
                        label: "USD/PLN exchange rate",
                    },
                ],
            };
        },
        watch: { //render chart when there is data, destroy when not first
            resultsData() {
                if (this.chart != null)
                    this.chart.destroy();

                if (this.resultsData.length > 0)
                    this.renderRatesChart();
            },
        },
        methods: {
            renderRatesChart() {
                var chartData = {
                    labels: [],
                    datasets: [
                        {
                            label: "USD/PLN exchange rate over time",
                            data: [],
                            backgroundColor: "#42b983"
                        },
                    ],
                };

                for (let entry of this.resultsData) {
                    chartData.labels.push(entry.date);
                    chartData.datasets[0].data.push(entry.rate);
                }

                var ctx = this.$refs.ratesChart.getContext("2d");
                this.chart = new Chart(ctx, {
                    type: "bar",
                    data: chartData,
                    options: {
                        scales: {
                            xAxes: [
                                {
                                    scaleLabel: {
                                        display: true,
                                        labelString: "Date [YYYY-MM-DD]",
                                        
                                    },
                                },
                            ],
                            yAxes: [
                                {
                                    scaleLabel: {
                                        display: true,
                                        labelString: "USD/PLN exchange rate",
                                    },
                                },
                            ],
                        },
                    },
                });
            },
        },
    };
</script>

<style scoped>
    .rates-chart {
        margin: 0 25% 50px 25%;
    }

    .table {
        max-width: 600px;
        margin-left: 34.3%;
    }
</style>
