from rest_framework import serializers
from .models import ExchangeRate
#
#
# class ExchangeRateSerializer(serializers.Serializer):
#     date = serializers.DateField()
#     rate = serializers.DecimalField(decimal_places=4, max_digits=10)
#
#     def create(self, validated_data):
#         return ExchangeRate.objects.create(validated_data)
#
#     def update(self, instance, validated_data):
#         instance.date = validated_data.get('date', instance.date)
#         instance.rate = validated_data.get('rate', instance.rate)
#         instance.save()
#         return instance


class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = ['date', 'rate', 'interpolated', 'volumePLN', 'volumeUSD']
