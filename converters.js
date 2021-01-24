function convertUSDChart(json) {
    var data = [];
    var keys = Object.keys(json)
    var values = Object.values(json)

    data.push(['Date', 'Rates'])
    for (var i = 0; i < keys.length; i++) {
        data.push([keys[i], values[i]['rate']])
    }
    return data
}

function convertUSDTable(json) {
    var data = [];
    var keys = Object.keys(json)
    var values = Object.values(json)

    for (var i = 0; i < keys.length; i++) {
        data.push([keys[i], values[i]['rate'], values[i]['interpolated']])
    }
    return data
}

function convertSalesChart(json) {
    var data = [];
    var keys = Object.keys(json)
    var values = Object.values(json)

    data.push(['Date', 'PLN', 'USD'])
    for (var i = 0; i < keys.length - 2; i++) {
        data.push([keys[i], values[i]['PLN'], values[i]['USD']])
    }
    return data
}

function convertSalesTable(json) {
    var data = [];
    var keys = Object.keys(json)
    var values = Object.values(json)

    for (var i = 0; i < keys.length - 2; i++) {
        data.push([keys[i], values[i]['PLN'], values[i]['USD']])
    }
    return data
}