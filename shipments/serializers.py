from rest_framework import serializers

from .models import Shipment, Article


# Serializer for Article model with the specified fields
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['name', 'quantity', 'price', 'sku']


# Serializer for Shipment model with related articles included
class ShipmentSerializer(serializers.ModelSerializer):
    # Nested serializer for related articles
    articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Shipment
        fields = ['tracking_number', 'carrier', 'sender_address', 'receiver_address', 'status', 'articles']
