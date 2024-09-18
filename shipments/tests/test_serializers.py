from unittest import TestCase
from rest_framework.exceptions import ValidationError
from ..serializers import ShipmentSerializer, ArticleSerializer, UserSerializer
from ..models import Shipment, Article


class ShipmentSerializerTests(TestCase):

    def setUp(self):
        self.shipment = Shipment.objects.create(
            tracking_number='TN12345678',
            carrier='DHL',
            sender_address='Street 1, 10115 Berlin, Germany',
            receiver_address='Street 10, 75001 Paris, France',
            status='in-transit'
        )

    def test_valid_shipment_serializer(self):
        serializer = ShipmentSerializer(instance=self.shipment)
        data = serializer.data
        self.assertEqual(data['tracking_number'], 'TN12345678')
        self.assertEqual(data['carrier'], 'DHL')

    def test_invalid_shipment_serializer(self):
        invalid_data = {
            'tracking_number': '',
            'carrier': 'DHL',
            'sender_address': 'Street 1, 10115 Berlin, Germany',
            'receiver_address': 'Street 10, 75001 Paris, France',
            'status': 'in-transit'
        }
        serializer = ShipmentSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class ArticleSerializerTests(TestCase):

    def setUp(self):
        self.shipment = Shipment.objects.create(
            tracking_number='TN12345679',
            carrier='UPS',
            sender_address='Street 2, 20144 Hamburg, Germany',
            receiver_address='Street 20, 1000 Brussels, Belgium',
            status='inbound-scan'
        )
        self.article = Article.objects.create(
            shipment=self.shipment,
            name='Monitor',
            quantity=2,
            price=200,
            sku='MT789'
        )

    def test_valid_article_serializer(self):
        serializer = ArticleSerializer(instance=self.article)
        data = serializer.data
        self.assertEqual(data['name'], 'Monitor')
        self.assertEqual(data['quantity'], 2)
        self.assertEqual(data['price'], 200)
        self.assertEqual(data['sku'], 'MT789')

    def test_article_serializer_with_invalid_data(self):
        invalid_data = {
            'shipment': self.shipment.id,
            'name': '',
            'quantity': -1,
            'price': -200,
            'sku': 'MT789'
        }
        serializer = ArticleSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
