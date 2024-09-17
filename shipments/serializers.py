# shipments/serializers.py
from rest_framework import serializers

from .models import Shipment, Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['name', 'quantity', 'price', 'sku']


class ShipmentSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Shipment
        fields = ['tracking_number', 'carrier', 'sender_address', 'receiver_address', 'status', 'articles']
