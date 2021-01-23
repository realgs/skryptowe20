import axios from 'axios';

const url = 'http://localhost:5000/'

export function getRates(date_from, date_to) {
    var req_url = url + 'rates/from/' + formatDate(date_from) + '/to/' + formatDate(date_to); 
    return axios.get(req_url);
}

export function getIncome(date_from, date_to) {
    var req_url = url + 'profits/from/' + formatDate(date_from) + '/to/' + formatDate(date_to); 
    return axios.get(req_url);
}

function formatDate(date) {
    const ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(date);
    const mo = new Intl.DateTimeFormat('en', { month: '2-digit' }).format(date);
    const da = new Intl.DateTimeFormat('en', { day: '2-digit' }).format(date);
    return `${ye}-${mo}-${da}`;
}