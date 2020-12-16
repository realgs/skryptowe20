API_URL = "http://api.nbp.pl/api/exchangerates/rates"

DAY_IN_SEC = 86400
MAX_DAYS = 6588
MIN_DAYS = 0
FETCH_DAYS_LIMIT = 350

DATE_FORMAT = "%Y-%m-%d"

DEFAULT_TABLE = "A"

AVAIL_CURRENCIES = {
    "AFN", "EUR", "ALL", "DZD", "USD", "AOA", "XCD", "ARS", "AMD", "AWG", "AUD", "AZN", "BSD", "BHD",
    "BDT", "BBD", "BYN", "BZD", "XOF", "BMD", "INR", "BTN", "BOB", "BOV", "BAM", "BWP", "NOK", "BRL",
    "BND", "BGN", "BIF", "CVE", "KHR", "XAF", "CAD", "KYD", "CLP", "CLF", "CNY", "COP", "COU", "KMF",
    "CDF", "NZD", "CRC", "HRK", "CUP", "CUC", "ANG", "CZK", "DKK", "DJF", "DOP", "EGP", "SVC", "ERN",
    "SZL", "ETB", "FKP", "FJD", "XPF", "GMD", "GEL", "GHS", "GIP", "GTQ", "GBP", "GNF", "GYD", "HTG",
    "HNL", "HKD", "HUF", "ISK", "IDR", "XDR", "IRR", "IQD", "ILS", "JMD", "JPY", "JOD", "KZT", "KES",
    "KPW", "KRW", "KWD", "KGS", "LAK", "LBP", "LSL", "ZAR", "LRD", "LYD", "CHF", "MOP", "MKD", "MGA",
    "MWK", "MYR", "MVR", "MRU", "MUR", "XUA", "MXN", "MXV", "MDL", "MNT", "MAD", "MZN", "MMK", "NAD",
    "NPR", "NIO", "NGN", "OMR", "PKR", "PAB", "PGK", "PYG", "PEN", "PHP", "PLN", "QAR", "RON", "RUB",
    "RWF", "SHP", "WST", "STN", "SAR", "RSD", "SCR", "SLL", "SGD", "XSU", "SBD", "SOS", "SSP", "LKR",
    "SDG", "SRD", "SEK", "CHE", "CHW", "SYP", "TWD", "TJS", "TZS", "THB", "TOP", "TTD", "TND", "TRY",
    "TMT", "UGX", "UAH", "AED", "USN", "UYU", "UYI", "UYW", "UZS", "VUV", "VES", "VND", "MAD", "YER",
    "ZMW", "ZWL", "XBA", "XBB", "XBC", "XBD", "XTS", "XXX", "XAU", "XPD", "XPT", "XAG"}

MSG_ERROR_INVALID_CURRENCY = f"Currency must be one of available values: \n{AVAIL_CURRENCIES}"
MSG_ERROR_INVALID_DAYS = f"Days have to be greater than {MIN_DAYS} and less than 18 years ({MAX_DAYS} days)!"
MSG_ERROR_FAILED_TO_FETCH = "Error fetching data!"

DATABASE_PATH = "Lab5/myApi/logic/Northwind2.sqlite"
