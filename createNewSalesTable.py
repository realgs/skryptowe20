import sqlite3

def createNewSalesTable():
     conn = sqlite3.connect('Cortland.db')
     cursor = conn.cursor()
     cursor.execute('''CREATE TABLE AllSales(Id,Date, USDsales, PLNsales);''')
     conn.commit()
     cursor.execute('''SELECT Iphone_11.Date, Iphone_11.Numbers_Sold, Iphone_11.Iphone_Price, CurrencyWithInterpolated.Currency
                              FROM Iphone_11 JOIN CurrencyWithInterpolated ON Iphone_11.Date = CurrencyWithInterpolated.Date''')
     USDamount = {}
     PLNamount = {}

     for row in cursor:
          if row[0] is not None:
               USDamount[str(row[0])] = row[1] * row[2] 
               PLNamount[str(row[0])] = round(row[1] * row[2] * row[3],2)

     id = 0
     for date, salesValue in USDamount.items():
          id+=1
          conn.execute("INSERT INTO AllSales (Id,Date, USDsales, PLNsales)\
                         VALUES(?,?,?,?)", (id, date, salesValue, PLNamount[date]))
     conn.commit()
     conn.close()
