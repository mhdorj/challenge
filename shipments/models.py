from django.db import models


class Shipment(models.Model):
    tracking_number = models.CharField(max_length=50)
    carrier = models.CharField(max_length=50)
    sender_address = models.CharField(max_length=255)
    receiver_address = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.tracking_number


class Article(models.Model):
    shipment = models.ForeignKey(Shipment, related_name='articles', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50)

    def __str__(self):
        return self.name
