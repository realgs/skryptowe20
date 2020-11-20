import requests
import datetime

MIN_AVAILABLE_DATE = "2002-01-02"
MAX_DAYS = 93


def format_datetime_to_string(date):
    return date.strftime("%Y-%m-%d")


def make_get_request_for_range(currency_code, start_date, end_date):
    start_date_string = format_datetime_to_string(start_date)
    end_date_string = format_datetime_to_string(end_date)
    response = requests.get(
        "http://api.nbp.pl/api/exchangerates/rates/a/{}/{}/{}/?format=json".format(currency_code, start_date_string,
                                                                                   end_date_string))
    if response.status_code == 200:
        result = []
        rates = response.json()["rates"]
        for single_day_data in rates:
            result.append((single_day_data["effectiveDate"], single_day_data["mid"]))
        return result
    else:
        return []


def split_dates_by_max_days(start_date, end_date):
    split_dates = []

    while (end_date - start_date).days > MAX_DAYS:
        split_dates.append((start_date, start_date + datetime.timedelta(days=MAX_DAYS)))
        start_date += datetime.timedelta(days=(MAX_DAYS + 1))

    split_dates.append((start_date, end_date))
    return split_dates


def get_exchange_rates_from_api(currency_code, start_date, end_date):
    if end_date < start_date:
        return []

    split_dates = split_dates_by_max_days(start_date, end_date)

    exchange_rates = []
    for single_date_range in split_dates:
        single_range_exchange = (make_get_request_for_range(currency_code, single_date_range[0], single_date_range[1]))
        exchange_rates.extend(single_range_exchange)

    return exchange_rates


if __name__ == "__main__":
    start = datetime.date(2020, 1, 1)
    end = datetime.date(2020, 10, 10)
    exchange_rates_from_api = get_exchange_rates_from_api("usd", start, end)

    for rate in exchange_rates_from_api:
        print(rate)
