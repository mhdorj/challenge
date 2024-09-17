import os
import csv
from django.core.management.base import BaseCommand
from shipments.models import Shipment, Article


class Command(BaseCommand):
    help = 'Load shipment data from a CSV file'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(base_dir)
        csv_file_path = os.path.join(base_dir, 'shipments.csv')

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                shipment, created = Shipment.objects.get_or_create(
                    tracking_number=row['tracking_number'],
                    carrier=row['carrier'],
                    sender_address=row['sender_address'],
                    receiver_address=row['receiver_address'],
                    status=row['status'],
                )
                Article.objects.create(
                    shipment=shipment,
                    name=row['article_name'],
                    quantity=row['article_quantity'],
                    price=row['article_price'],
                    sku=row['SKU'],
                )
