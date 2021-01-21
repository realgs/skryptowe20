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
