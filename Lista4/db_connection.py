import pyodbc as db

if __name__ == '__main__':
    conn = db.connect('Driver={SQL Server};'
                      'Server=DESKTOP-AKTNFDK;'
                      'Database=AdventureWorksLT2019;'
                      'Trusted_Connection=yes;')

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM AdventureWorksLT2019.SalesLT.SalesOrderHeader')

    for row in cursor:
        print(row)
