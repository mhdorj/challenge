from django.contrib import admin
from .models import Shipment, Article


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'carrier', 'sender_address', 'receiver_address', 'status')
    search_fields = ('tracking_number', 'carrier', 'status')
    list_filter = ('carrier', 'status')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'sku', 'shipment')
    search_fields = ('name', 'sku')
    list_filter = ('shipment',)
