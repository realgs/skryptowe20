from datetime import datetime

SUPPORTED_CURRENCY_CODES = {'EUR', 'USD', 'CHF', 'GBP', 'TRY', 'AUD', 'RUB'}
VALID_DATE_FORMAT = "%Y-%m-%d"
DATE_PARAM = 'date'
START_DATE_PARAM = 'startDate'
END_DATE_PARAM = 'endDate'
EARLIEST_START_DATE = datetime.fromisocalendar(2012, 1, 2).date()
MAX_DAYS_DELTA = 365


def validate_rates_request_params(currency_code, params):
    errors = []
    if currency_code not in SUPPORTED_CURRENCY_CODES:
        errors.append(
            f"Currency code: {currency_code} is not supported. All available currencies: {SUPPORTED_CURRENCY_CODES}")
    if START_DATE_PARAM not in params:
        errors.append(f"Parameter: {START_DATE_PARAM} has to be specified.")
    elif not is_validate_date(params[START_DATE_PARAM]):
        errors.append(f"Parameter: {START_DATE_PARAM} is not a valid date.")
    if END_DATE_PARAM not in params:
        errors.append(f"Parameter: {END_DATE_PARAM} has to be specified.")
    elif not is_validate_date(params[END_DATE_PARAM]):
        errors.append(f"Parameter: {END_DATE_PARAM} is not a valid date.")
    return errors


def is_validate_date(date_text):
    try:
        if date_text != datetime.strptime(date_text, VALID_DATE_FORMAT).strftime(VALID_DATE_FORMAT):
            raise ValueError
        return True
    except ValueError:
        return False


def validate_rates_request_dates(start_date, end_date):
    errors = []
    current_date = datetime.now().date()
    if start_date > end_date:
        errors.append(f"{START_DATE_PARAM} cannot be greater than the {END_DATE_PARAM}.")
    if start_date > current_date or end_date > current_date:
        errors.append(f"Either {START_DATE_PARAM} or {END_DATE_PARAM} cannot relate to the future.")
    elif start_date < EARLIEST_START_DATE and end_date < EARLIEST_START_DATE:
        errors.append(f"Either {START_DATE_PARAM} or {END_DATE_PARAM} cannot be lower than ${EARLIEST_START_DATE}.")
    if (end_date - start_date).days > MAX_DAYS_DELTA:
        errors.append(
            f"Number of days between {START_DATE_PARAM} and {END_DATE_PARAM} cannot be grater than {MAX_DAYS_DELTA}."
        )
    return errors


def validate_rates_request(currency_code, params):
    errors = validate_rates_request_params(currency_code, params)
    if len(errors) == 0:
        start_date = datetime.strptime(params[START_DATE_PARAM], VALID_DATE_FORMAT).date()
        end_date = datetime.strptime(params[END_DATE_PARAM], VALID_DATE_FORMAT).date()
        errors.extend(validate_rates_request_dates(start_date, end_date))
        if len(errors) == 0:
            return True, {
                "currencyCode": currency_code,
                "startDate": start_date,
                "endDate": end_date
            }
    return False, errors


def validate_sales_request(currency_code, params):
    errors = []
    current_date = datetime.now().date()
    if currency_code not in SUPPORTED_CURRENCY_CODES:
        errors.append(
            f"Currency code: {currency_code} is not supported. All available currencies: {SUPPORTED_CURRENCY_CODES}")
    if DATE_PARAM not in params:
        errors.append(f"Parameter: {DATE_PARAM} has to be specified.")
    elif not is_validate_date(params[DATE_PARAM]):
        errors.append(f"Parameter: {DATE_PARAM} is not a valid date.")
    if len(errors) == 0:
        date = datetime.strptime(params[DATE_PARAM], VALID_DATE_FORMAT).date()
        if date < EARLIEST_START_DATE:
            errors.append(f"{DATE_PARAM} cannot be lower than ${EARLIEST_START_DATE}.")
        elif date > current_date:
            errors.append(f"{DATE_PARAM} cannot relate to the future.")
        if len(errors) == 0:
            return True, {"currencyCode": currency_code, "date": date}
    return False, errors
