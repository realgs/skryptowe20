from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'currency', views.CurrencyViewSet)
router.register(r'sales', views.DailySalesViewSet)

urlpatterns = [
    path('', views.index),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('rate/<str:one_date>', views.getJsonRate),
    path('rate/<str:from_date>/<str:to_date>', views.getJsonRateTwoDates),
    path('sale/<str:one_date>', views.getJsonSale),
    path('sale/<str:from_date>/<str:to_date>', views.getJsonSaleTwoDates),
    path('readme', views.readme)
]
