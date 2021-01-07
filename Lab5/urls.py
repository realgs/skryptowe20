from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from APIApp.views import TestView

urlpatterns = [
    path('api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('',TestView.as_view(), name='Kursy waluty'),
    path('<str:oper>/<str:date>',TestView.as_view())
]
