from datetime import datetime
import currency_api


def parse_str_to_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()


if __name__ == '__main__':
    str_date_from = "2019-11-05"
    str_date_to = "2019-11-12"

    date_from = parse_str_to_date(str_date_from)
    date_to = parse_str_to_date(str_date_to)
    currency_api.get_currency_rates('GBP', date_from, date_to)
