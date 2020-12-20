from xml.etree.ElementInclude import include
from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from Api.RateEndpoint import Rate
from Api.SalesEndpoint import Sales
from Api.MultiDatesRateEndpoint import MultiRate
from Api.MultiSalesEndpoint import MultiSales

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('', Rate.as_view()),
    path('sales/', Sales.as_view()),
    path('rate/', Rate.as_view()),
    path('rate/<str:date>', Rate.as_view()),
    path('rate/dates/', MultiRate.as_view()),
    path('sales/<str:day>', Sales.as_view()),
    path('rate/dates/<str:fromDate>/<str:toDate>', MultiRate.as_view()),
    path('sales/dates/<str:fromDate>/<str:toDate>', MultiSales.as_view()),

]
