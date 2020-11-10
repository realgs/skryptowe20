import requests
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import sqlite3

def createUsdToPlnTable():
    conn = sqlite3.connect('sales_data.db')
    cursor = conn.cursor()
    print("Database connected")

    cursor.execute('''CREATE TABLE UsdToPln (ID, EffectiveDate, CurrencyValue);''')
    print("Table created")
    conn.commit()
    
    result = {}
    current_date = datetime.strptime('2014-12-31', '%Y-%m-%d')
    end_date = datetime.strptime('2011-01-01', '%Y-%m-%d')
    
    while(current_date>end_date):
        print("Fetching date: "+current_date.strftime("%Y-%m-%d"))
        resp = requests.get('http://api.nbp.pl/api/exchangerates/rates/A/USD/{}/'.format(current_date.strftime("%Y-%m-%d")))
        if resp.status_code != 200:
            result[current_date.strftime("%Y-%m-%d")] = prev_resp.json()['rates'][0]['mid']
        else:
            prev_resp = resp
            result[current_date.strftime("%Y-%m-%d")] = resp.json()['rates'][0]['mid']

        current_date = current_date - timedelta(days=1)

    lp = 0
    for key, value in result.items():
        lp+=1
        current_date = datetime.strptime(key, '%Y-%m-%d')
        conn.execute("INSERT INTO UsdToPln (ID, EffectiveDate, CurrencyValue) \
                     VALUES (?, ?, ?)", (lp, current_date.strftime("%d-%m-%Y"), value))
    conn.commit()
    conn.close()

def createSalesDiagram():
    sales_pln = {}
    sales_usd = {}
    conn = sqlite3.connect('sales_data.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT SalesOrders.OrderDate, SalesOrders.TotalDue, UsdToPln.CurrencyValue  
                      FROM SalesOrders JOIN UsdToPln ON SalesOrders.OrderDate=UsdToPln.EffectiveDate''')

    print("Reading data from table...")
    for row in cursor:
        if row[1] is not None:
            if str(row[0]) not in sales_usd:
                sales_usd[str(row[0])] = row[1]
            else:
                sales_usd[str(row[0])] += row[1]

            if str(row[0]) not in sales_pln:
                sales_pln[str(row[0])] = row[1]*row[2]
            else:
                sales_pln[str(row[0])] += (row[1]*row[2])

    plotSales(sales_usd, sales_pln)

def plotSales(usd_dict, pln_dict):
    usd_dates = []
    usd_rates = []
    pln_dates = []
    pln_rates = []
    print("Creating plot...")
    for key, value in usd_dict.items():
        usd_dates.append(key)
        usd_rates.append(value)

    for key, value in pln_dict.items():
        pln_dates.append(key)
        pln_rates.append(value)

    fig, ax = plt.subplots()
    plt.figure(figsize=(16,6))
    
    dollar_line, = plt.plot(usd_rates, 'g', label='USD')
    euro_line, = plt.plot(pln_rates, 'r', label='PLN')
    plt.xlabel('Dates')
    ax.xaxis.set_label_coords(1.05, -0.025)
    usd_dates_short = usd_dates[::100]
    plt.xticks(range(0, len(usd_dates), 100), usd_dates_short)
    plt.xticks(rotation=45)
    plt.xticks(fontsize=6)
    plt.ylabel('Sales')
    plt.title('USD and PLN sales')
    plt.legend(handles=[dollar_line, euro_line])
    plt.savefig("usd_pln_figure.svg")
