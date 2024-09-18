from django.core.cache import cache

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import requests
from decouple import config

from .models import Shipment, Article
from .permissions import IsAuthenticatedForWriteOnly
from .serializers import ShipmentSerializer, ArticleSerializer


class ShipmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling shipment-related operations including listing and filtering shipments.
    """
    queryset = Shipment.objects.all().prefetch_related('articles')
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticatedForWriteOnly]

    def get_queryset(self):
        """
        Optionally filter shipments by tracking number and carrier.
        """
        queryset = super().get_queryset()
        tracking_number = self.request.query_params.get('tracking_number')
        carrier = self.request.query_params.get('carrier')

        if tracking_number:
            queryset = queryset.filter(tracking_number=tracking_number)
        if carrier:
            queryset = queryset.filter(carrier=carrier)
        return queryset

    @action(detail=True, methods=['get'])
    def weather(self, request, pk=None):
        """
        Retrieve weather information based on the shipment's receiver address.
        """
        shipment = self.get_object()
        receiver_address = shipment.receiver_address

        try:
            zip_code = receiver_address.split(' ')[-1]
        except IndexError:
            return Response(
                {"error": "Could not extract zip code from address"},
                status=400
            )

        cache_key = f'weather_{zip_code}'
        cached_weather = cache.get(cache_key)
        if cached_weather:
            return Response(cached_weather)

        api_key = config('WEATHER_API_KEY')
        base_url = config('WEATHER_API_URL')
        url = f'{base_url}?q={zip_code}&appid={api_key}'
        weather_response = requests.get(url)

        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            cache.set(cache_key, weather_data, timeout=7200)
            return Response(weather_data)

        return Response(
            {"error": "City not found or invalid API request"},
            status=weather_response.status_code
        )


class ArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling article-related operations including listing and creating articles.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedForWriteOnly]
