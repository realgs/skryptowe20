import pyodbc as db
import datetime
import matplotlib.pyplot as plt
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


# Zadanie 5 - dzienne zarobki sklepu
def draw_profit_diagram():
    cursor = conn.cursor()
    cursor.execute("""SELECT [orders].[order_date] AS day_in_year, 
    SUM([order_items].[list_price]*[order_items].[quantity]) AS profit_usd, 
    SUM([order_items].[list_price]*[order_items].[quantity]*[rates].[measure_rate]) AS profit_pln
    FROM [BikeStores].[sales].[orders] 
    JOIN [BikeStores].[sales].[order_items] 
    ON [BikeStores].[sales].[orders].[order_id] = [BikeStores].[sales].[order_items].[order_id]
    JOIN [BikeStores].[dbo].[rates] 
    ON [BikeStores].[sales].[orders].[order_date] = [BikeStores].[dbo].[rates].[measure_date]
    GROUP BY [orders].[order_date]
    HAVING [orders].[order_date] BETWEEN '2017-01-01' AND '2017-06-30'
    ORDER BY [orders].[order_date]""")

    data_time = []
    data_dollar = []
    data_pln = []
    for row in cursor:
        data_time.append(row[0])
        data_dollar.append(row[1])
        data_pln.append(row[2])

    plt.title('Łączna sprzedaż sklepów rowerowych w PLN i USD z okresu 2017-01-01 - 2017-06-30')
    plt.xlabel('Data')
    plt.ylabel('Łączna sprzedaż')
    plt.xticks(range(len(data_time))[::10], rotation=35)
    plt.plot(data_time, data_dollar, label='USD')
    plt.plot(data_time, data_pln, label='PLN')
    plt.legend()
    plt.savefig('bike_shops_profits.svg', format='svg')
    plt.show()


if __name__ == '__main__':
    # Database created with:
    # https://www.sqlservertutorial.net/sql-server-sample-database/
    conn = db.connect('Driver={SQL Server};'
                      'Server=DESKTOP-AKTNFDK;'
                      'Database=BikeStores;'
                      'Trusted_Connection=yes;')

    # Add database table and fill it
    table_data = get_average_currency_rates_between('USD', datetime.date(2015, 12, 20), datetime.date(2018, 1, 4))
    create_rates_table(table_data)

    # Generate diagram for profits
    draw_profit_diagram()
