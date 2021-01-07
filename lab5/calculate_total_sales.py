import sqlite3


def __get_total_sales(sales, exchange_rates):
    records = []

    sales_index = 0
    for (date, rate) in exchange_rates:
        if sales_index < len(sales) and date == sales[sales_index][0]:
            total_sales_usd = sales[sales_index][1]
            total_sales_pln = round(total_sales_usd * rate, 4)
            sales_count = sales[sales_index][2]

            records.append((date, total_sales_usd, total_sales_pln, sales_count))
            sales_index += 1
        else:
            records.append((date, 0, 0, 0))

    return records


if __name__ == '__main__':
    connection = sqlite3.connect('chinook.db')
    cursor = connection.cursor()
    cursor.execute(
        "SELECT date, price FROM exchange_rate WHERE date BETWEEN '2009-01-01' AND '2010-12-31' ORDER BY date")
    exchange_rates = cursor.fetchall()

    cursor.execute(
        "SELECT strftime('%Y-%m-%d', InvoiceDate), SUM(Total), COUNT(*) FROM invoices GROUP BY InvoiceDate HAVING InvoiceDate BETWEEN '2009-01-01' AND '2010-12-31'")
    sales = cursor.fetchall()

    total_sales = __get_total_sales(sales, exchange_rates)
    total_sales_string = str(total_sales)[1:-1]
    cursor.execute('CREATE TABLE total_sales(date text, sales_usd real, sales_pln real, number_of_sales integer)')
    cursor.execute('INSERT INTO total_sales VALUES {}'.format(total_sales_string))

    connection.commit()
    connection.close()

