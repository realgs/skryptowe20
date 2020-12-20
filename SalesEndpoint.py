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
l = 5

output = "Wrong value"

def sales(date):
        output = {}
        conn = sqlite3.connect('Cortland.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT Id,Date, USDsales, PLNsales
                                     FROM AllSales''')
        for elem in cursor:
            if elem[1] == date:
                output['ID'] = elem[0]
                output['Date'] = date
                output['In PLN sales'] = elem[2]
                output['IN USD sales'] = elem[3]
        conn.close()
        return output

class Sales(APIView):
    def get(self, request, day = '2019-05-07'):
        data = sales(day)
        if data == None or data == {}:
            data = {
                output: day
            } 
        return Response(data)