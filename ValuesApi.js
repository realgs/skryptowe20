function rateValue() {
    fetch('http://127.0.0.1:8000/rate/').then(response => response.json())
        .then(value => {
            document.querySelector('#output').innerHTML = value["Rate USD"];
        })
}

function salesValue() {
    fetch('http://127.0.0.1:8000/sales/').then(response => response.json())
        .then(value => {
            document.querySelector('#salesUSD').innerHTML = value["In PLN sales"];
            document.querySelector('#salesPLN').innerHTML = value["IN USD sales"];
        })
}

function rateDate() {
    var temp = document.querySelector('#RateDate').value;
    var url = 'http://127.0.0.1:8000/rate/';
    var merged = url.concat(temp);

    fetch(merged).then(response => response.json())
        .then(value => {
            document.querySelector('#output2').innerHTML = value["Rate USD"];
            if (value["Wrong link"] == temp)
                document.querySelector('#output2').innerHTML = "Błędna data lub format";
        })
}

function rateSalesDate() {
    var temp = document.querySelector('#SalesDateRange').value;
    var url = 'http://127.0.0.1:8000/sales/';
    var merged = url.concat(temp);

    fetch(merged).then(response => response.json())
        .then(value => {
            document.querySelector('#salesUSDoutput').innerHTML = value["In PLN sales"];
            document.querySelector('#salesPLNoutput').innerHTML = value["IN USD sales"];

            if (value["Wrong value"] == temp) {
                document.querySelector('#salesUSDoutput').innerHTML = "Błędna data lub format";
                document.querySelector('#salesPLNoutput').innerHTML = "Błędna data lub format";
            }
        })
}

function rateMulti() {

    var temp = document.querySelector('#multi1').value;
    var temp2 = document.querySelector('#multi2').value;
    var tt = "/";
    var url = 'http://127.0.0.1:8000/rate/dates/';
    var merged = url.concat(temp, tt, temp2);
    fetch(merged).then(response => response.json())
        .then(value => {
            if (value["Wrong value"] == "Wrong link") {
                document.querySelector('#outputRange').innerHTML = "Błędna data lub format";
                document.querySelector('#outputRange2').innerHTML = "Błędna data lub format";
            } else {


                var element_count = 0;

                const daty = value.map(e => e.Date);
                const rate = value.map(e => e.Rate);
                var merged = "";
                var mergedV = "";

                var count = 0;
                var index = 1;

                for (var prop in daty) {
                    if (daty.hasOwnProperty(prop))
                        ++count;
                }

                for (var i = 0; i < count; i++) {

                    merged = merged.concat(index + ". " + daty[i].toString() + " | ");
                    mergedV = mergedV.concat(index + ". " + rate[i].toString() + " | ");
                    index++;

                }
                document.querySelector('#outputRange').innerHTML = merged;
                document.querySelector('#outputRange2').innerHTML = mergedV;
            }

        })
}

function salesMulti() {

    var temp = document.querySelector('#multiSales').value;
    var temp2 = document.querySelector('#multiSales2').value;
    var tt = "/";
    var url = 'http://127.0.0.1:8000/sales/dates/';
    var merged = url.concat(temp, tt, temp2);
    fetch(merged).then(response => response.json())
        .then(value => {
            if (value["Wrong value"] == "Wrong link") {
                document.querySelector('#outputRangeSales').innerHTML = "Błędna data lub format";
                document.querySelector('#outputRangeSales2').innerHTML = "Błędna data lub format";
                document.querySelector('#outputRangeSales3').innerHTML = "Błędna data lub format";

            } else {
                var element_count = 0;
                const daty = value.map(e => e.Date);
                const rate = value.map(e => e.USD);
                const rate2 = value.map(e => e.PLN);
                var merged = "";
                var mergedV = "";
                var mergedV2 = "";

                var count = 0;
                var index = 1;

                for (var prop in daty) {
                    if (daty.hasOwnProperty(prop))
                        ++count;
                }

                for (var i = 0; i < count; i++) {
                    merged = merged.concat(index + ". " + daty[i].toString() + " | ");
                    mergedV = mergedV.concat(index + ". " + rate[i].toString() + " | ");
                    mergedV2 = mergedV2.concat(index + ". " + rate2[i].toString() + " | ");
                    index++;
                }
                document.querySelector('#outputRangeSales').innerHTML = merged;
                document.querySelector('#outputRangeSales2').innerHTML = mergedV;
                document.querySelector('#outputRangeSales3').innerHTML = mergedV2;
            }

        })
}
document.querySelector('#submit').onclick = () => rateValue();
document.querySelector('#rateSubmit').onclick = () => rateDate();
document.querySelector('#sales').onclick = () => salesValue();
document.querySelector('#sales2').onclick = () => rateSalesDate();
document.querySelector('#multi').onclick = () => rateMulti();
document.querySelector('#multiSal').onclick = () => salesMulti();

