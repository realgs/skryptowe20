import sqlite3
import matplotlib.pyplot as matplotlib

def createChartUSDPLN():
    
    tempUSDate = []
    currencyUSD = []
    tempPLNDate = []
    currencyPLN = []
    plnToDrow = {}
    usdToDrow = {}
    
    conn = sqlite3.connect('Cortland.db')
    c = conn.cursor()

    c.execute('''SELECT Phones.Date, Phones.Pay, AverageRateToPLN.Value
                    FROM Phones JOIN AverageRateToPLN ON Phones.Date=AverageRateToPLN.DateCurrency''')

    for unit in c:
        if str(unit[0]) not in usdToDrow:
            usdToDrow[str(unit[ 0 ])] = unit[ 1 ]
        else:
            usdToDrow[str(unit[ 0 ])] += unit[ 1 ]
        if str(unit[0]) not in plnToDrow:
            plnToDrow[str(unit[ 0 ])] = unit[ 1 ]*unit[ 2]
        else:
            plnToDrow[str(unit[ 0 ])] += (unit[ 1 ]*unit[ 2 ])
    
    fig, yx = matplotlib.subplots()

    for first, second in usdToDrow.items():
        tempUSDate.append(first)
        currencyUSD.append(second)

    for first, second in plnToDrow.items():
        tempPLNDate.append(first)
        currencyPLN.append(second)

    
    matplotlib.figure( figsize = (20,9))
    matplotlib.xticks( rotation = 30 )

    matplotlib.xlabel('Date [YYYY-MM-DD]')
    matplotlib.ylabel('Sales values')
    matplotlib.title('Sales')

    wykrDolar, = matplotlib.plot(currencyUSD, 'b', label='Dollar')
    wykrEuro, = matplotlib.plot(currencyPLN, 'g', label='PLN')

    usd_dates_short = tempUSDate[::40]
    matplotlib.xticks( range(0, len(tempUSDate), 40), usd_dates_short)
    matplotlib.legend( handles = [wykrDolar, wykrEuro])

    matplotlib.savefig("wykres2.svg")

def halfYearChartEuroDolar(arrDolars, arrEuro):
    
    datesDolars = []
    datesEuro = []

    valuesDolar = []
    valuesEuro = []

    ag, yx = matplotlib.subplots()

    for first, second in arrDolars.items():
        datesDolars.append(first)
        valuesDolar.append(second)

    for first, second in arrEuro.items():
        datesEuro.append(first)
        valuesEuro.append(second)

    
    matplotlib.figure( figsize = (20, 9) )
    matplotlib.xticks( rotation = 30 )

    wykrEuro, = matplotlib.plot( datesEuro, valuesEuro, 'g', label = 'Euro')
    wykrDolar, = matplotlib.plot( datesDolars, valuesDolar, 'b', label = 'Dollar')
    

    matplotlib.ylabel('Rate [PLN]')
    matplotlib.title('Euro and Dollar')
    matplotlib.xlabel('Date [YYYY-MM-DD]')

    matplotlib.legend( handles = [wykrDolar, wykrEuro])
  
    datesIntervalDown = datesDolars[::8]
    matplotlib.xticks( range(0, len(datesDolars), 8), datesIntervalDown )
    
    matplotlib.savefig("wykres1.svg")
