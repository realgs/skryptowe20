import sqlite3
import request

def createDailySalesTable():
    conn = sqlite3.connect('sales_data.db')
    #conn.execute("""DROP TABLE DailySales""")
    #print("Table dropped")
    conn.execute("""CREATE TABLE IF NOT EXISTS DailySales(
                    sales_id integer PRIMARY KEY,
                    salesdate text,
                    plnsales integer,
                    usdsales integer) """)
    print("Table created")
    
def insertIntoDailySalesTable():
    sales_pln = {}
    sales_usd = {}

    conn = sqlite3.connect('sales_data.db')
    cursor = conn.cursor()

    cursor.execute("""DELETE FROM DailySales""")
    print("Previous data deleted")
    conn.commit()

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
                sales_pln[str(row[0])] = int(row[1]*row[2])
            else:
                sales_pln[str(row[0])] += int((row[1]*row[2]))

    print("Inserting data to table...")
    for saledate in sales_pln:
        conn.execute("INSERT INTO DailySales(salesdate, plnsales, usdsales) \
                    VALUES(?, ?, ?)", \
                    (saledate, sales_pln[saledate], sales_usd[saledate]))
    conn.commit()
    conn.close()

def selectDailySalesTable():
    conn = sqlite3.connect('sales_data.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM DailySales""") 
    column_names = [desc[0] for desc in cursor.description]
    print(column_names)
    for row in cursor:
        print(str(row[0])+"\t"+str(row[1])+"\t"+str(row[2])+"\t"+str(row[3]))

def checkDatabase():
    con = sqlite3.connect('sales_data.db')
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())

def createUsdToPlnTableInterpolated():
    conn = sqlite3.connect('sales_data.db')
    cursor = conn.cursor()
    print("Database connected")

    cursor.execute('''CREATE TABLE UsdToPln (ID, EffectiveDate, CurrencyValue, Interpolated);''')
    print("Table created")
    conn.commit()
    
    result = {}
    interpolated = {}
    prev_resp = None
    missing_dates = []
    current_date = datetime.strptime('2014-12-31', '%Y-%m-%d')
    end_date = datetime.strptime('2011-01-01', '%Y-%m-%d')
    
    while(current_date>end_date):
        print("Fetching date: "+current_date.strftime("%Y-%m-%d"))
        resp = requests.get('http://api.nbp.pl/api/exchangerates/rates/A/USD/{}/'.format(current_date.strftime("%Y-%m-%d")))
        if resp.status_code != 200:
            if prev_resp == None:
                missing_dates.append(current_date.strftime("%Y-%m-%d"))
            else:
                result[current_date.strftime("%Y-%m-%d")] = prev_resp.json()['rates'][0]['mid']
                interpolated[current_date.strftime("%Y-%m-%d")] = 1
        else:
            if missing_dates != []:
                for date in missing_dates:
                    result[date] = resp.json()['rates'][0]['mid']
                missing_dates.clear()
            prev_resp = resp
            result[current_date.strftime("%Y-%m-%d")] = resp.json()['rates'][0]['mid']
            interpolated[current_date.strftime("%Y-%m-%d")] = 0

        current_date = current_date - timedelta(days=1)

    lp = 0
    for key, value in result.items():
        lp+=1
        current_date = datetime.strptime(key, '%Y-%m-%d')
        conn.execute("INSERT INTO UsdToPln (ID, EffectiveDate, CurrencyValue, Interpolated) \
                     VALUES (?, ?, ?, ?)", (lp, current_date.strftime("%d-%m-%Y"), value, interpolated[key]))
    conn.commit()
    conn.close()
