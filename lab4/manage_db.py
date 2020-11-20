import db_init
import plot_data
from datetime import datetime, timedelta
import data


def add_weekend_rates(currency_data):
    data_len = len(currency_data)
    for i in range(data_len):
        print(type(currency_data[i]['effectiveDate']))
        prev_date = datetime.strptime(currency_data[i]['effectiveDate'], "%Y-%m-%d")
        next_date = datetime.strptime(currency_data[i + 1]['effectiveDate'], "%Y-%m-%d")
        if next_date - prev_date > timedelta(days=1):
            print(prev_date)
            print(next_date)
            currency_data.insert(i + 1, {'effectiveDate': datetime.strftime(prev_date + timedelta(days=1), "%Y-%m-%d"),
                                         'mid': currency_data[i]['mid']})
            data_len += 1
    return currency_data


def main():
    db_init.init_db()
    currency_data = data.get_currency_from_period('usd', date_from='2004-05-06', date_to='2005-05-07')
    currency_data = add_weekend_rates(currency_data)
    print(currency_data)
    db_init.add_curr_rate_table(currency_data)
    plot_data.plot()


if __name__=="__main__":
    main()