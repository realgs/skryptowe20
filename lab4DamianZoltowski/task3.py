import matplotlib.pyplot as plt

def drawChart(currency1Data, currency2Data, timeSpan):
    time = range(0, timeSpan)
    plt.plot(time, currency1Data[0], color='red', label=currency1Data[1].json()['currency'])
    plt.plot(time, currency2Data[0], color='blue', label=currency2Data[1].json()['currency'])
    plt.xlabel('Days', fontsize=14)
    plt.ylabel('Currency value', fontsize=14)
    plt.legend()
    plt.title(f'Currency exchange values for {currency1Data[1].json()["currency"]} and {currency2Data[1].json()["currency"]}')
    plt.savefig("task3.svg")
    plt.show()
