from django.test import TestCase
from ..models import Shipment, Article


class ShipmentModelTests(TestCase):

    def setUp(self):
        self.shipment = Shipment.objects.create(
            tracking_number='TN12345678',
            carrier='DHL',
            sender_address='Street 1, 10115 Berlin, Germany',
            receiver_address='Street 10, 75001 Paris, France',
            status='in-transit'
        )

    def test_shipment_creation(self):
        self.assertEqual(self.shipment.tracking_number, 'TN12345678')
        self.assertEqual(self.shipment.carrier, 'DHL')
        self.assertEqual(self.shipment.status, 'in-transit')

    def test_str_method(self):
        self.assertEqual(str(self.shipment), 'TN12345678')


class ArticleModelTests(TestCase):

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

    def test_article_creation(self):
        self.assertEqual(self.article.name, 'Monitor')
        self.assertEqual(self.article.quantity, 2)
        self.assertEqual(self.article.price, 200)
        self.assertEqual(self.article.sku, 'MT789')

    def test_article_relationship(self):
        self.assertEqual(self.article.shipment, self.shipment)
