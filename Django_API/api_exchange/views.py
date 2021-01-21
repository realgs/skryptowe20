from django.http import HttpResponse

from .models import ExchangeRate
from .serializers import ExchangeRateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

@api_view(['GET', 'POST'])
def exchange_rates_list(request):
    if request.method == 'GET':
        rates = ExchangeRate.objects.all()
        serializer = ExchangeRateSerializer(rates, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ExchangeRateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def exchange_rates_list_date_filtered(request, date_from, date_to):
    print(date_from)
    print(date_to)
    try:
        rates = ExchangeRate.objects.filter(date__range=[date_from, date_to])
    except ExchangeRate.DoesNotExist:
        return HttpResponse(status=404)
    serializer = ExchangeRateSerializer(rates, many=True)
    return Response(serializer.data)
