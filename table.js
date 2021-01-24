google.charts.load('current', { 'packages': ['table'] });

function drawTableUSD(dataTable) {
    console.log(dataTable)
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Date');
    data.addColumn('number', 'Rate');
    data.addColumn('string', 'Interpolated');
    data.addRows(dataTable);

    var table = new google.visualization.Table(document.getElementById('table_div'));

    table.draw(data, { showRowNumber: true, width: '100%', height: '100%' });
}

function drawTableSales(dataTable) {
    console.log(dataTable)
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Date');
    data.addColumn('number', 'PLN');
    data.addColumn('number', 'USD');
    data.addRows(dataTable);

    var table = new google.visualization.Table(document.getElementById('table_div'));

    table.draw(data, { showRowNumber: true, width: '100%', height: '100%' });
}