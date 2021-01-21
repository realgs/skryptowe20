from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('currencies_and_sales.urls')),
    path('admin/', admin.site.urls),
]
