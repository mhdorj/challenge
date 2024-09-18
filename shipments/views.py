from django.contrib.auth import logout, login, authenticate
from django.db import models
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
import requests
from decouple import config
from .models import Shipment, Article
from .permissions import IsAuthenticatedForWriteOnly
from .serializers import ShipmentSerializer, ArticleSerializer, UserSerializer


# Shipment and Article Models (same as before)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "User created successfully"})
        return Response(serializer.errors, status=400)

    # Login with Session only
    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            # Login with session
            login(request, user)
            return Response({"status": "Logged in successfully using session"})
        else:
            return Response({"error": "Invalid credentials"}, status=401)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        # Logout for session
        logout(request)
        return Response({"status": "Logged out successfully from session"})

    @action(detail=True, methods=['delete'])
    def unregister(self, request, pk=None):
        user = self.get_object()
        user.delete()
        return Response({"status": "User deleted successfully"})


class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all().prefetch_related('articles')
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticatedForWriteOnly]

    def get_queryset(self):
        """Optional filtering logic by tracking number and carrier"""
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
        url = f'https://api.openweathermap.org/data/2.5/weather?q={zip_code}&appid={api_key}'
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
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedForWriteOnly]
