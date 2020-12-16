from django.urls import path
from . import views

urlpatterns = [
    path('', views.test, name='test'),
    path('<str:currency_code>/<slug:start_date>/<slug:end_date>/', views.history, name='history'),
]
