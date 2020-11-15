import matplotlib.pyplot as plt
from ApiService import getUsdAndEurOverHalfOfYear


def generateUsdAndEurOverHalfOfYearPlot():
    (usd, eur) = getUsdAndEurOverHalfOfYear()
    (usdMid, usdDates, eurMid, eurDates) = getDataLists(usd, eur)

    plt.scatter(
        usdDates, usdMid, c="blue", edgecolor="black", linewidths=1, label="USD"
    )

    plt.scatter(
        eurDates, eurMid, c="red", edgecolor="black", linewidths=1, label="EUR"
    )

    plt.title("Plot of average EUR and USD exchange rates over the last six months")
    plt.xlabel("Date")
    plt.ylabel("Exchange rate")
    plt.legend()
    plt.savefig("UsdAndEurOverHalfOfYear.svg")
    plt.show()


def getDataLists(usd, eur):
    usdMid = []
    usdDates = []
    eurMid = []
    eurDates = []
    for u in usd:
        usdMid.append(u.mid)
        usdDates.append(u.effectiveDate)
    for e in eur:
        eurMid.append(e.mid)
        eurDates.append(e.effectiveDate)
    return usdMid, usdDates, eurMid, eurDates


if __name__ == '__main__':
    generateUsdAndEurOverHalfOfYearPlot()
