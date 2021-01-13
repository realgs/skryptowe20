from xml.etree.ElementInclude import include
from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from ApiApp.views import TestView

from ApiApp import views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('home', TestView.as_view()),
    path('', TestView.as_view(), name='test'),
    path('<str:curr>/<str:days>', TestView.as_view())
]
