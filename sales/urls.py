from django.urls import path
from django.views.decorators.cache import cache_page
from . import views


urlpatterns = [
        path('currency/', cache_page(60 * 15)(views.CurrencyRangeList.as_view({'get': 'list'}))),
        path('sales/', cache_page(60 * 15)(views.SalesStatGetView.as_view({'get': 'list'}))),
        ]
