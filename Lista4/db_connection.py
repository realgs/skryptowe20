import pyodbc as db
import datetime
from api_connection import get_average_currency_rates_between


# Zadanie 4 - modyfikacja istniejcej bazy danych
def create_rates_table(data):
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE BikeStores.dbo.rates ('
                   'measure_date DATE NOT NULL PRIMARY KEY,'
                   'measure_rate DECIMAL (7, 4) NOT NULL);')

    query = 'INSERT INTO BikeStores.dbo.rates(measure_date,measure_rate) VALUES(?,?)'

    for idx in range(len(data)):
        cursor.execute(query, (data[idx]['effectiveDate'], float(data[idx]['mid'])))
        if idx < len(data) - 1:
            date_idx0 = datetime.datetime.strptime(data[idx]['effectiveDate'], '%Y-%m-%d')
            date_idx1 = datetime.datetime.strptime(data[idx+1]['effectiveDate'], '%Y-%m-%d')
            date_diff = (date_idx1 - date_idx0).days
            for excess in range(date_diff - 1):
                date_idx0 += datetime.timedelta(days=1)
                cursor.execute(query, (date_idx0, float(data[idx]['mid'])))

    conn.commit()


if __name__ == '__main__':
    # Database created with:
    # https://www.sqlservertutorial.net/sql-server-sample-database/
    conn = db.connect('Driver={SQL Server};'
                      'Server=DESKTOP-AKTNFDK;'
                      'Database=BikeStores;'
                      'Trusted_Connection=yes;')

    #for row in cursor:
    #    print(row)
    table_data = get_average_currency_rates_between('USD', datetime.date(2015, 12, 20), datetime.date(2018, 1, 4))
    create_rates_table(table_data)
