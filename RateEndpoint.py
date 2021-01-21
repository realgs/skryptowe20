import sqlite3
import requests
import json
import datetime
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions

output = "Wrong link"

def getRates(days):
    rates = {}
    conn = sqlite3.connect('Cortland.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT ID, Date, Currency, Interpolated
                 FROM CurrencyWithInterpolated''')
    for elem in cursor:
        if elem[1] == days:
            rates['ID'] = elem[0]
            rates['Date'] = elem[1]
            rates['Rate USD'] = elem[2] 
            if elem[3] == True:
                rates['Interpolated'] = True
            else:
                rates['Interpolated'] = False
    return rates

class Rate(APIView):  

    def get(self, request, date = '2019-05-11'):
        data = getRates(date)
        if data == None or data == {}:
            data = {
                output: date
            } 
        return Response(data)

