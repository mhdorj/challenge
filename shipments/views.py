# shipments/views.py
from django.core.cache import cache
from rest_framework import viewsets
from .models import Shipment
from .serializers import ShipmentSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
from django.utils import timezone
from datetime import timedelta


class ShipmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    @action(detail=True, methods=['get'])
    def weather(self, request, pk=None):
        shipment = self.get_object()
        zip_code = shipment.receiver_address.split(', ')[-1]

        # Caching mechanism
        cache_key = f'weather_{zip_code}'
        cached_weather = cache.get(cache_key)
        if cached_weather and timezone.now() < cached_weather['timestamp'] + timedelta(hours=2):
            return Response(cached_weather['data'])

        # Fetch weather data
        api_key = '2a6bbd7debb745f4a452208cbcf2e036'
        weather_response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?zip={zip_code}&appid={api_key}')
        weather_data = weather_response.json()

        # Cache the data
        cache.set(cache_key, {'data': weather_data, 'timestamp': timezone.now()})

        return Response(weather_data)
