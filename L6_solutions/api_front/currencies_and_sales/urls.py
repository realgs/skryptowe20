"""api_front URL Configuration

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
from django.urls import path
from currencies_and_sales import views

app_name = 'currencies_and_sales'

urlpatterns = [
    path('', views.index, name="index"),
    path('single_date_rates', views.rates_single_date, name="single_date_rates"),
    path('date_range_rates', views.rates_date_range, name="date_range_rates"),
    path('single_date_sales', views.sales_single_date, name="single_date_sales"),
    path('date_range_sales', views.sales_date_range, name="date_range_sales"),

]
