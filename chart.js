google.charts.load('current', { 'packages': ['corechart'] })

function drawChart(dataTable, optionsSet) {
    var data = google.visualization.arrayToDataTable(dataTable);

    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(data, optionsSet);
}