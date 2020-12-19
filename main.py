from datetime import datetime
import currency_api


def parse_str_to_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()


if __name__ == '__main__':
    str_date_from = "2020-11-07"
    str_date_to = "2020-11-08"

    date_from = parse_str_to_date(str_date_from)
    date_to = parse_str_to_date(str_date_to)
    currency_api.get_currency_rates('USD', date_from, date_to)
