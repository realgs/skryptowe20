from database import Database
import sqlite3


if __name__ == "__main__":
  db_source = "../../Source/bazunia.db"

  start_date = '2012-07-04'
  end_date = '2014-05-06'

  db = Database(db_source)
  db.create_avg_currency_rates_table()
  db.insert_usd_rates(start_date, end_date)
