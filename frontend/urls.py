from django.urls import path
from . import views


urlpatterns = [
        path('', views.index),
        path('currency/', views.index),
        path('sales/', views.index),
        ]
