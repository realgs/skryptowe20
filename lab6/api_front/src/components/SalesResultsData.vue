<template>
    <div>
        <div class="sales-chart" v-if="resultsData">
            <canvas ref="salesChart"></canvas>
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
        name: "SalesResultsData",
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
                        key: "sales_pln",
                        label: "Sales in PLN [zl]",
                    },
                    {
                        key: "sales_usd",
                        label: "Sales in USD [$]",
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
                            label: "Sales in USD",
                            data: [],
                            backgroundColor: "#336600"
                        },
                        {
                            label: "Sales in PLN",
                            data: [],
                            backgroundColor: "#591cc1"
                        },
                    ],
                };

                for (let entry of this.resultsData) {
                    chartData.labels.push(entry.date);
                    chartData.datasets[0].data.push(entry.sales_pln);
                    chartData.datasets[1].data.push(entry.sales_usd);
                }

                var ctx = this.$refs.salesChart.getContext("2d");
                this.chart = new Chart(ctx, {
                    type: "bar",
                    data: chartData,
                    options: {
                        title: {
                            display: true,
                            text: "Sales in both PLN and USD over time",
                        },
                        scales: {
                            xAxes: [
                                {
                                    offset: true,
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
                                        labelString: "Total sales in PLN and USD",
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
    .sales-chart {
        margin: 0 20% 50px 20%;
    }

    .table {
        max-width: 600px;
        margin-left: 34.3%;
    }
</style>
