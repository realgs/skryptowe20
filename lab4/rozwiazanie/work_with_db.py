import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='classicmodels',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `orders`"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
finally:
    connection.close()
