import task1, task3, task4, task5

if __name__ == '__main__':
    days = 182
    usdData = task1.averageExchangeRate('usd', days)
    eurData = task1.averageExchangeRate('eur', days)
    print(f"Exchange rates for currency {usdData[1].json()['currency']} for the last {days} days are following:")
    print(usdData[0])
    print(f"Exchange rates for currency {eurData[1].json()['currency']} for the last {days} days are following:")
    print(eurData[0])
    task3.drawChart(usdData, eurData, days)
    task4.createTableCurrencyQuotes()
    task4.fillTableWithData()
    task5.drawSalesChart()
