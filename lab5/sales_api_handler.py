import datetime as dt

MY_DB_DATE_FROM = "2011-10-01"
MY_DB_DATE_TO = "2014-05-28"
AVAILABLE_CURRENCIES = ['AUD', 'BYN', 'BGN', 'HRK', 'DKK',
                        'JPY', 'CAD', 'NOK', 'CZK', 'RUB',
                        'RON', 'PLN', 'CHF', 'SEK', 'TRY',
                        'EUR', 'UAH', 'HUF', 'GBP']


def create_error_json(currency, date):
    currency_is_correct = __check_currency_available(currency)
    dates_format = __check_date_format(date)

    if not currency_is_correct:
        if dates_format:
            return __create_error_message("Invalid currency. Currency not found."), 404
        return __create_error_message("Invalid request"), 400
    if not dates_format:
        return __create_error_message("Invalid date format. Admissible: YYYY-MM-DD"), 400
    if dates_format:
        dates_range = __check_date_range(date)
        if not dates_range:
            return __create_error_message("Data out of range selected. Allowed range from " +
                                          MY_DB_DATE_FROM + " to " + MY_DB_DATE_TO), 400

    return None


def __check_currency_available(currency):
    return AVAILABLE_CURRENCIES.__contains__(str(currency))


def __check_date_format(date):
    if len(date) == 10:
        for i in range(len(date)):
            if not (i == 4 or i == 7):
                if not date[i].isnumeric():
                    return False
    else:
        return False
    return True


def __check_date_range(date):
    date_to_check = dt.datetime.strptime(date, '%Y-%m-%d')
    if date_to_check < dt.datetime.strptime(MY_DB_DATE_FROM, '%Y-%m-%d') or \
            date_to_check > dt.datetime.strptime(MY_DB_DATE_TO, '%Y-%m-%d'):
        return False
    return True


def __create_error_message(message):
    return {"message": message}
