from db.models import *
from django.db.models import *
from django.core import serializers
import requests
import json

def api_send(shop,order):
    products_queryset = CellProduct.objects.all().filter(order=order)
    products = serializers.serialize('json', products_queryset)
    senddate = {
        "shop_code":shop.code,
        "date":order.create,
        "order_id":order.id,
        "money_total":order.total_price,
        "money_cs":order.cs_price,
        "money_remainig":order.remaining_price,
        "products":products
    }
    url = shop.webhock
    response = requests.post(url, data=senddate)
    return response



