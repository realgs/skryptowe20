from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def test(request):
    return HttpResponse("Test tylko tutaj hehe")

def history(request, currency_code, start_date, end_date):
    return HttpResponse(f"Zapytales o {currency_code} z przedzialu od {start_date} do {end_date}")