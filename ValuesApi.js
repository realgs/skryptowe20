function rateValue()
{
    fetch('http://127.0.0.1:8000/rate/').then( response =>  response.json())
    .then(value => {
        document.querySelector('#output').innerHTML = value["Rate USD"];
    })

}

function salesValue()
{
    fetch('http://127.0.0.1:8000/sales/').then(response =>  response.json())
    .then(value => {
        document.querySelector('#salesUSD').innerHTML = value["In PLN sales"];
        document.querySelector('#salesPLN').innerHTML = value["IN USD sales"];
    })
}

function rateRangeDate()
{
    const merged = "";
    const url ='http://127.0.0.1:8000/rate/dates/2019-05-03/2019-05-06';
    fetch(url).then( response =>  response.json())
    .then(value => {
        
        var element_count = 0;
        for(var e in value)
            if(value.hasOwnProperty(e))
                element_count++;

        for(var i = 0; i < element_count; i++)
        {
            var data = value[i]["Date"];         
            var rate = value[i]["Rate"];

            merged = merged.concat(data.toString());
            merged = merged.concat(rate.toString());    
            console.log(merged);
            console.log("xs");
        }
        console.log(merged);
        document.querySelector('#outputRange').innerHTML = merged;    
    })
}

function rateDate()
{
    var temp = document.querySelector('#RateDate').value;
    var url ='http://127.0.0.1:8000/rate/';
    var merged = url.concat(temp);

    fetch(merged).then( response =>  response.json())
    .then(value => {
        console.log(value);
        document.querySelector('#output2').innerHTML = value["Rate USD"];
    })
}

function rateSalesDate()
{
    var temp = document.querySelector('#SalesDateRange').value;
    var url ='http://127.0.0.1:8000/sales/';
    var merged = url.concat(temp);

    fetch(merged).then( response =>  response.json())
    .then(value => {
        console.log(value)
        document.querySelector('#salesUSDoutput').innerHTML = value["In PLN sales"];
        document.querySelector('#salesPLNoutput').innerHTML = value["IN USD sales"];
    })
}

document.querySelector('#submit').onclick =() => rateValue();
document.querySelector('#rateSubmit').onclick =() => rateDate();
document.querySelector('#sales').onclick =() => salesValue();
document.querySelector('#sales2').onclick =() => rateSalesDate();