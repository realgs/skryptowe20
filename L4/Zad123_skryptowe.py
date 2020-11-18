import requests
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt

def averageExchangeRatesForXDays (currency,XDays):
    current=datetime.datetime.now()
    currentDate=makeDate(current)    
    date=current-datetime.timedelta(days=(XDays+1))
    thisDate=makeDate(date)
    resp=requests.get("http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{thisDate}/{currentDate}/?format=json".format(currency=currency,thisDate=thisDate,currentDate=currentDate))
    if(resp.status_code!=200): raise Exception('Error {} url nbp api'.format(resp.status_code))
    else: 
        print('{}'.format(resp.text))
        return resp

def averageExchangeRates (currency,lastdays):
    resp=[]
    if (lastdays>200):
        while (lastdays>200):
            resp.append(averageExchangeRatesForXDays(currency,200).text)
            lastdays-=200
        resp.append(averageExchangeRatesForXDays(currency,lastdays).text)       
    else: 
        resp.append(averageExchangeRatesForXDays(currency,lastdays).text)
    return resp

def makeDate(date):
    thisDate=date.strftime("%Y-%m-%d")
    return thisDate

def drawChart(respUSD,respEUR, days):
    xUSD=[]
    yUSD=[]
    i=0
    xEUR=[]
    yEUR=[]
    j=0
    (xUSD,yUSD)=toListForLine(respUSD,xUSD,yUSD,i)
    (xEUR,yEUR)=toListForLine(respEUR,xEUR,yEUR,j)
    plt.plot(xUSD,yUSD)
    plt.plot(xEUR,yEUR)
    xUSDShort=xUSD[::15]
    plt.xticks(range(0,len(xUSD),15),xUSDShort)  
    plt.xlabel('Dates')
    plt.ylabel('Averae Exchange Rates')
    plt.legend(['USD Rates','EUR Rates'])
    plt.title('Chart of average USD and EUR rates from last {days} days'.format(days=days))
    plt.grid(True)
    plt.gcf().autofmt_xdate(rotation=25)
    plt.savefig("USD-EUR_Chart.svg")
    plt.show()
    
def toListForLine(resp,x,y,i):
    while(i<len(resp)):
        data=resp[i]
        text=json.loads(data)
        for elem in text['rates']:
            y.append(elem['mid'])
        
        for elem in text['rates']:
            x.append(elem['effectiveDate'])
        i+=1
    return (x,y)

if __name__=='__main__':
    days=int(366/2)
    #averageExchangeRates("usd",days)
    #averageExchangeRates("eur",days)
    drawChart(averageExchangeRates("usd",days),averageExchangeRates("eur",days),days)
