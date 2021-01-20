"""salesapi URL Configuration

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
from django.urls import path, include
from rest_framework.authtoken import views
# from rest_framework import routers
# from sales import views



# router = routers.DefaultRouter()
# router.register(r'CurrencyRange', views.CurrencyRangeList)
# router.register(r'SaleStats', views.SalesStatGetView)


urlpatterns = [
    # path('', include(router.urls)),
    path('api/', include('sales.urls')),
    path('api-token-auth/', views.obtain_auth_token, name='api-tokn-auth'),
    path('', include('frontend.urls')),

    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
