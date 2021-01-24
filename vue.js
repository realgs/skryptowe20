var yesterday = new Date()
yesterday.setDate(yesterday.getDate() - 1)

var app = new Vue({
    el: '#app',
    delimeters: ['[[', ']]'],
    data: {
        startDateSales: "2012-07-04",
        endDateSales: "2016-02-19",
        startRatingsDate: "2002-01-02",
        endRatingsDate: yesterday.toISOString().slice(0, 10),

        startDate: "2016-02-19",
        endDate: "2016-02-19"
    },
    methods: {
        fetchUSDRatesData() {
            var options = {
                title: 'USD Rates',
                curveType: 'function',
                legend: { position: 'bottom' },
            };
            if (this.startDate == this.endDate) {
                $.getJSON('http://127.0.0.1:5000/rates/USD/' + this.startDate, function (json) {
                    drawChart(convertUSDChart(json), options)
                    drawTableUSD(convertUSDTable(json))
                })
            }
            else if (this.startDate > this.endDate) {
                $.getJSON('http://127.0.0.1:5000/rates/USD/' + this.endDate + '/' + this.startDate, function (json) {
                    drawChart(convertUSDChart(json), options)
                    drawTableUSD(convertUSDTable(json))
                })
            }
            else {
                $.getJSON('http://127.0.0.1:5000/rates/USD/' + this.startDate + '/' + this.endDate, function (json) {
                    drawChart(convertUSDChart(json), options)
                    drawTableUSD(convertUSDTable(json))
                })
            }
        },
        fetchSalesData() {
            var options = {
                title: 'Sales',
                curveType: 'function',
                legend: { position: 'bottom' },
            };
            if (this.startDate == this.endDate) {
                $.getJSON('http://127.0.0.1:5000/sales/' + this.startDate, function (json) {
                    drawChart(convertSalesChart(json), options)
                    drawTableSales(convertSalesTable(json))
                })
            }
            else if (this.startDate > this.endDate) {
                $.getJSON('http://127.0.0.1:5000/sales/' + this.endDate + '/' + this.startDate, function (json) {
                    drawChart(convertSalesChart(json), options)
                    drawTableSales(convertSalesTable(json))
                })
            }
            else {
                $.getJSON('http://127.0.0.1:5000/sales/' + this.startDate + '/' + this.endDate, function (json) {
                    drawChart(convertSalesChart(json), options)
                    drawTableSales(convertSalesTable(json))
                })
            }
        },
        sales() {
            document.getElementById("salesPicker").style = "visibility: display;";
            document.getElementById("ratesPicker").style = "visibility: hidden;";
            this.startDate = this.endDateSales;
            this.endDate = this.endDateSales;
        },
        rates() {
            document.getElementById("salesPicker").style = "visibility: hidden;";
            document.getElementById("ratesPicker").style = "visibility: display;";
            this.startDate = this.endRatingsDate;
            this.endDate = this.endRatingsDate;
        },
        setStartDate(e) {
            this.startDate = e.toString();
        },
        setEndDate(e) {
            this.endDate = e.toString();
        }
    }
})