import db_init
import plot_data
from datetime import datetime, timedelta
import data


def add_weekend_rates(currency_data):
    data_len = len(currency_data)
    for row in currency_data:
        if currency_data.index(row) < data_len - 1:
            prev_date = datetime.strptime(row['effectiveDate'], "%Y-%m-%d")
            next_date = datetime.strptime(currency_data[currency_data.index(row)+1]['effectiveDate'], "%Y-%m-%d")
            if next_date - prev_date > timedelta(days=1):
                currency_data.insert(currency_data.index(row) + 1,
                                     {'effectiveDate': datetime.strftime(prev_date + timedelta(days=1), "%Y-%m-%d"),
                                      'mid': row['mid'], 'interpolated': True})
                data_len += 1
    return currency_data


def main():
    db_init.init_db()
    currency_data = data.get_currency_from_period('usd', date_from='2004-05-05', date_to='2005-05-07')
    currency_data = add_weekend_rates(currency_data)
    db_init.add_curr_rate_table(currency_data)
    plot_data.plot()


if __name__ == "__main__":
    main()
