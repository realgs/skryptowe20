import pyodbc as db
import datetime
import matplotlib.pyplot as plt
from api_connection import get_average_currency_rates_between


# Database created with:
# https://www.sqlservertutorial.net/sql-server-sample-database/
conn = db.connect('Driver={SQL Server};'
                'Server=DESKTOP-AKTNFDK;'
                'Database=BikeStores;'
                'Trusted_Connection=yes;')


# Zadanie 4 - modyfikacja istniejcej bazy danych
def create_rates_table(data):
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE BikeStores.dbo.rates ('
                   'measure_date DATE NOT NULL PRIMARY KEY,'
                   'measure_rate DECIMAL (7, 4) NOT NULL,'
                   'interpolated BIT NOT NULL);')
    conn.commit()

    update_rates_table(data)

# Added option to add interpolation from db in case update_rates_table_to_today is called on weekend
def update_rates_table(data, interpolate_date=None):
    cursor = conn.cursor()
    query = 'INSERT INTO BikeStores.dbo.rates(measure_date,measure_rate, interpolated) VALUES(?,?,?)'

    for idx in range(len(data)):
        cursor.execute(query, (data[idx]['effectiveDate'], float(data[idx]['mid']), 0))
        if idx < len(data) - 1:
            date_idx0 = datetime.datetime.strptime(data[idx]['effectiveDate'], '%Y-%m-%d')
            date_idx1 = datetime.datetime.strptime(data[idx+1]['effectiveDate'], '%Y-%m-%d')
            date_diff = (date_idx1 - date_idx0).days
            for excess in range(date_diff - 1):
                date_idx0 += datetime.timedelta(days=1)
                cursor.execute(query, (date_idx0, float(data[idx]['mid']), 1))
    
    # interpolate_date -> date of last rate that will be stored in db
    if interpolate_date != None:
        # if there is option, interpolate from data list passed as arg
        if (len(data) > 0):
            last_date = datetime.datetime.strptime(data[-1]['effectiveDate'], '%Y-%m-%d')
            for excess in range((interpolate_date - last_date).days):
                last_date += datetime.timedelta(days=1)
                cursor.execute(query, (last_date, float(data[-1]['mid']), 1))
        # otherwise take last rate from db
        else:
            cursor.execute('SELECT TOP (1) [measure_date],[measure_rate] FROM [BikeStores].[dbo].[rates] ORDER BY [measure_date] DESC;')
            last_tuple = cursor.fetchone()
            if last_tuple != None:
                last_date = datetime.datetime.strptime(last_tuple[0], '%Y-%m-%d')
                for excess in range((interpolate_date - last_date).days):
                    last_date += datetime.timedelta(days=1)
                    cursor.execute(query, (last_date, float(last_tuple[1]), 1))


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

    plt.title('Przychód sklepów rowerowych w PLN i USD; 2017-01-01 - 2017-06-30')
    plt.xlabel('Data')
    plt.ylabel('Łączna sprzedaż')
    plt.xticks(range(len(data_time))[::20], rotation=20)
    plt.plot(data_time, data_dollar, label='USD')
    plt.plot(data_time, data_pln, label='PLN')
    plt.legend()
    plt.savefig('bike_shops_profits.svg', format='svg')
    plt.show()


def update_rates_table_to_day(day):
    cursor = conn.cursor()
    # Get most recent date in table
    cursor.execute("""SELECT TOP (1) [measure_date]
    FROM [BikeStores].[dbo].[rates]
    ORDER BY [measure_date] DESC""")

    last_date = cursor.fetchone()
    if last_date != None:
        last_date = datetime.datetime.strptime(last_date[0], '%Y-%m-%d')
        if (day > last_date):
            table_data = get_average_currency_rates_between('USD', last_date + datetime.timedelta(days=1), day)
            update_rates_table(table_data, day)


def get_rates_from_to(date_from, date_to):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM [BikeStores].[dbo].[rates] '
    'WHERE [measure_date] >= \'' + date_from + '\'' + 
    ' AND [measure_date] <= \'' + date_to + '\';')
    result = []
    for row in cursor:
        result.append({'date':datetime.datetime.strptime(row[0], '%Y-%m-%d'),'rate':row[1],'interpolated':False if row[2] == 0 else True})
    return result


def initialize_db():
    try:
        table_data = get_average_currency_rates_between('USD', datetime.date(2015, 12, 20), datetime.date(2018, 1, 4))
        create_rates_table(table_data)
    except Exception as ex:
        print("Error while initializing db")


if __name__ == '__main__':
    # Add database table and fill it
    initialize_db()

    # Generate diagram for profits
    draw_profit_diagram()
