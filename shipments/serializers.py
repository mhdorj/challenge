# shipments/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Shipment, Article


# Serializer for َUser model with the specified fields
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        # Ensure password is write-only for security
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create a user with the given validated data
        user = User.objects.create_user(**validated_data)
        return user


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
