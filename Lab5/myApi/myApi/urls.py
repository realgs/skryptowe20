"""myApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from logic import views
from logic.DataAPI import data_setup

urlpatterns = [
    path('rates/<str:currency_code>/<slug:start_date>/<slug:end_date>/', views.history, name='history'),
    path('summary/<str:currency_code>/<slug:date>/', views.summary, name='summary'),
    path('summary/<str:currency_code>/<slug:start_date>/<slug:end_date>/', views.summary, name='summary'),
]

data_setup.setup()
