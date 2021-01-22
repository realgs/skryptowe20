let apiLink = document.getElementById('api_link');
let responseArea = document.getElementById('response_value');
let apiTypeDropdown = document.getElementById('api_type_dropdown');
let currencyDropdown = document.getElementById('currency_dropdown');
let singleDateOnlyCheckbox = document.getElementById('single_date_only_checkbox');
let singleDate = document.getElementById('single_date');
let startDate = document.getElementById('start_date');
let endDate = document.getElementById('end_date');

async function generateLink() {
    let datesPart = getDatesPart();
    let apiTypePart = getApiTypePart();

    let link = `http://127.0.0.1:5000/api/${apiTypePart}/${datesPart}`;
    apiLink.value = link;


    const response = await fetch(link);
    const jsonResponse = await response.json()
    responseArea.value = JSON.stringify(jsonResponse);
}

function getDatesPart() {
    if (singleDateOnlyCheckbox.checked === true) {
        return singleDate.value;
    } else {
        return `${startDate.value}/${endDate.value}`
    }
}

function getApiTypePart() {
    if (apiTypeDropdown.value === 'sum') {
        return `${apiTypeDropdown.value}/${currencyDropdown.value}`;
    } else {
        return `${apiTypeDropdown.value}`
    }
}