from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Shipment, Article


class ShipmentViewSetTests(APITestCase):

    def setUp(self):
        # Create some test shipments and articles
        self.shipment1 = Shipment.objects.create(
            tracking_number='TN12345678',
            carrier='DHL',
            sender_address='Street 1, 10115 Berlin, Germany',
            receiver_address='Street 10, 75001 Paris, France',
            status='in-transit'
        )
        self.shipment2 = Shipment.objects.create(
            tracking_number='TN12345679',
            carrier='UPS',
            sender_address='Street 2, 20144 Hamburg, Germany',
            receiver_address='Street 20, 1000 Brussels, Belgium',
            status='inbound-scan'
        )
        self.article1 = Article.objects.create(
            shipment=self.shipment1,
            name='Laptop',
            quantity=1,
            price=800,
            sku='LP123'
        )
        self.article2 = Article.objects.create(
            shipment=self.shipment1,
            name='Mouse',
            quantity=1,
            price=25,
            sku='MO456'
        )

    def test_list_shipments(self):
        url = '/shipments/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_shipments_by_tracking_number(self):
        url = '/shipments/?tracking_number=TN12345678'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tracking_number'], 'TN12345678')

    def test_filter_shipments_by_carrier(self):
        url = '/shipments/?carrier=DHL'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['carrier'], 'DHL')

    def test_weather_endpoint(self):
        url = f'/shipments/{self.shipment1.id}/weather/'
        # Mocking requests.get response
        with self.settings(WEATHER_API_URL='https://api.openweathermap.org/data/2.5/weather',
                           WEATHER_API_KEY='testkey'):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            # Add further checks based on mocked response


class ArticleViewSetTests(APITestCase):

    def setUp(self):
        self.shipment = Shipment.objects.create(
            tracking_number='TN12345680',
            carrier='DPD',
            sender_address='Street 3, 80331 Munich, Germany',
            receiver_address='Street 5, 28013 Madrid, Spain',
            status='delivery'
        )
        self.article = Article.objects.create(
            shipment=self.shipment,
            name='Keyboard',
            quantity=1,
            price=50,
            sku='KB012'
        )

    def test_list_articles(self):
        url = '/articles/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_article(self):
        url = '/articles/'
        data = {
            'shipment': self.shipment.id,
            'name': 'Mouse',
            'quantity': 2,
            'price': 25,
            'sku': 'MO456'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Mouse')
