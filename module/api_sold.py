from db.models import *
from django.db.models import *
import requests
import json

def api_send(shop,order):
    producs = Product.objects.all().filter(order=order)
    senddate = {
        "shop_code":shop.code,
        "date":order.create,
        "order_id":order.id,
        "money_total":total_price,
        "money_cs":cs_price,
        "money_remainig":remaining_price,
        "products":products
    }
    url = shop.regi_post
    response = requests.post(url, data=senddate)
    return response



