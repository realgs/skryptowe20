from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "interface_app/home.html")


def request_builder(request):
    return render(request, "interface_app/request_builder.html")
