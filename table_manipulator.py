import sqlite3
import exchange_rates_acquirer as rates_acquirer
import datetime

MIN_DATE = datetime.date(2012, 7, 1)
MAX_DATE = datetime.date(2016, 2, 29)

CREATE_TABLE_QUERY = "CREATE TABLE ExchangeRate (date text, rate real, is_interpolated boolean)"
INSERT_QUERY = "INSERT INTO ExchangeRate (date, rate, is_interpolated) VALUES (?, ?, ?)"
DROP_TABLE_QUERY = "DROP TABLE ExchangeRate"
SELECT_SUM_OF_TRANSACTIONS_QUERY = """
SELECT 
ER.date transaction_date, ROUND(IFNULL(orderSum, 0), 2) usd_value, ROUND(IFNULL(orderSum, 0) * ER.rate, 2) pln_value 
FROM 
ExchangeRate ER LEFT JOIN 
(
SELECT DATE(O.OrderDate) innerDate, SUM(OD.UnitPrice * OD.Quantity) orderSum
FROM OrderDetail OD JOIN `Order` O ON OD.OrderId = O.Id
GROUP BY DATE(O.OrderDate)
) ON ER.date = innerDate
ORDER BY
ER.date;
"""


def get_rows_from_api(currency_code, start_date, end_date):
    api_rates = rates_acquirer.get_exchange_rates_from_api(currency_code, start_date, end_date)
    all_days_rates = rates_acquirer.expand_exchange_rates_to_range(api_rates, currency_code, start_date, end_date)

    return all_days_rates


def create_exchange_rates_table():
    connection = sqlite3.connect("NNorthwind.sqlite")
    cursor = connection.cursor()

    cursor.execute(DROP_TABLE_QUERY)

    cursor.execute(CREATE_TABLE_QUERY)

    rows = get_rows_from_api("usd", MIN_DATE, MAX_DATE)

    for row in rows:
        cursor.execute(INSERT_QUERY, row)

    connection.commit()

    cursor.close()
    connection.close()


if __name__ == "__main__":
    create_exchange_rates_table()
