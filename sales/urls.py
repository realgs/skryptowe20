from django.urls import path
from . import views


urlpatterns = [
        path('currency/', views.CurrencyRangeList.as_view({'get': 'list'})),
        path('sales/', views.SalesStatGetView.as_view({'get': 'list'})),
        ]
