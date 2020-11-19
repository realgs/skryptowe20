import requests
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt

def smallerPieceOfData (currency,lastDays):
    
    today=datetime.datetime.now()  
    todayDate=today.strftime("%Y-%m-%d")
    chosen=today-datetime.timedelta(days=(lastDays+1))
    chosenDate=chosen.strftime("%Y-%m-%d")
    resp=requests.get("http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{chosenDate}/{todayDate}/?format=json".format(currency=currency,chosenDate=chosenDate, todayDate=todayDate))
    if(resp.status_code!=200):
        raise Exception('Error {} url nbp api'.format(resp.status_code))
    else:
        print('{}'.format(resp.json()))
    return resp

def exchangeRates (currency, days):
    resp=[]
    if (days>185):
        
        while (days>185):
            resp.append(smallerPieceOfData(currency,185).text)
            days-=185
        resp.append(smallerPieceOfData(currency,days).text)
            
    else: 
        resp.append(smallerPieceOfData(currency,days).text)
    return resp

def chart(resp, resp2):
    x=[]
    y=[]
    x2=[]
    y2=[]
    i=0
    j=0
    while(i<len(resp)):
        data=resp[i]
        text=json.loads(data)
        
        for elem in text['rates']:
            y.append(elem['mid'])
        
        for elem in text['rates']:
            x.append(elem['effectiveDate'])
        
        i+=1
    while(j<len(resp2)):
        data=resp2[j]
        text=json.loads(data)
        
        for elem in text['rates']:
            y2.append(elem['mid'])
        
        for elem in text['rates']:
            x2.append(elem['effectiveDate'])
        
        j+=1
    plt.plot(x,y)
    plt.plot(x2, y2)
    shorter=x[::15]
    plt.xticks(range(0, len (x), 15), shorter)
    plt.title('Wykres notowań USD przez ostatnie dni')
    plt.xlabel('Daty notowań')
    plt.ylabel('Średnie kursy')
    plt.legend(['Notowanie dolara', 'Notowania euro'])
    
    plt.gcf().autofmt_xdate(rotation =25)
    plt.grid(True)
    plt.savefig("Chart-USD-EUR.svg")
    plt.show()

if __name__=='__main__':
    
    exchangeRates("usd", 183)
    exchangeRates("eur", 183)
    exchangeRates("usd", 370)
    chart(exchangeRates("usd", 183), exchangeRates("eur", 183))
