from database import Database
import sqlite3


if __name__ == "__main__":
  db_source = "../../Source/bazunia.db"

  db = Database(db_source)

  [(min_date, max_date)] = db.get_min_max_dates()

  db.create_avg_currency_rates_table()
  db.insert_rates(min_date, max_date)
