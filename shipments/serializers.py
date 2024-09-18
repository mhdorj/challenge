# shipments/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Shipment, Article


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['name', 'quantity', 'price', 'sku']


class ShipmentSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Shipment
        fields = ['tracking_number', 'carrier', 'sender_address', 'receiver_address', 'status', 'articles']
