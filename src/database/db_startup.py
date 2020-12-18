from datetime import datetime, timedelta
from nbp import fetch_currency_from_two_tables, from_json_to_list
import sqlite3


DB_NAME = "../../Source/bazunia.db"
DATEFORMAT = "%Y-%m-%d"


def _add_missing_dates(rates):
  for i in range(len(rates) - 1):
    curr = rates[i]
    next = rates[i + 1]

    curr_date = datetime.strptime(curr[1], DATEFORMAT)
    next_date = datetime.strptime(next[1], DATEFORMAT)
    delta = next_date - curr_date

    if delta.days > 1:
        next_day = curr_date + timedelta(days=1)
        rates.insert(i + 1, (
            curr[0],
            next_day.strftime(DATEFORMAT),
            True
        ))
  return rates


def insert_usd_rates(start_date, end_date):
  conn = sqlite3.connect(DB_NAME)
  c = conn.cursor()

  rates = fetch_currency_from_two_tables(start_date, end_date)
  new_rates = _add_missing_dates(rates)

  c.execute('SELECT * FROM AvgUsdRates')
  db_rates = c.fetchall()
  to_insert = new_rates - db_rates
  print(to_insert)

  c.executemany('INSERT INTO AvgUsdRates VALUES (?, ?, ?)', to_insert)
  conn.commit()


if __name__ == "__main__":
