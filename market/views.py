from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from db.models import *
from django.db.models import *
from django.db.models.functions import Coalesce
import datetime as dt 
from django.template.loader import render_to_string
from module.user_auth import *
from module.product_status import *

import hashlib
import json

# Create your views here.
@login_required
def market(request,shopCODE):
    if request.method == "POST":
        shop = Shop.objects.get(code=shopCODE)
        match request.POST["type"]:
            case "get_products":
                products = Product.objects.all().filter(Q(shop=shop)&Q(web_cart=True))
                param = {
                    "products":products,
                    'shop':shop
                }
                data = render_to_string("market/cart/products.html",param)
                return HttpResponse(data)
            case "add_cart":
                product = Product.objects.get(id=request.POST['id'])
                param = {
                    "product":product,
                    "number":request.POST["number"]
                }
                data = render_to_string("market/cart/cart_add_product.html",param)
                return HttpResponse(data)
            case "post_treasurer":
                shop = Shop.objects.get(code=shopCODE)
                order = Order.objects.create(
                    shop = Shop.objects.get(code=shopCODE),
                    customer = request.user,
                    status = "reserved",
                    day = '',
                    total_price = request.POST["total_price"],
                    number = request.POST["number"],
                    reserved_date = request.POST["reserved_date"],
                    secret = randomstr(10),
                    cs_price = 0,
                    remaining_price = 0
                )
                order.reserved_id = order.id + 1500
                order.save()

                def outofrange(order):
                    order.delete()

                for product_id,product_number in zip(json.loads(request.POST["products_ids"]),json.loads(request.POST["products_numbers"])):
                    product = Product.objects.get(id=product_id)
                    if int(product_stock(product)) < int(product_number):
                        outofrange(order)
                        return HttpResponse("outofrange")
                    if product.limit < int(product_number):
                        outofrange(order)
                        return HttpResponse("limit")
                    CellProduct.objects.create(
                        product=product,
                        order=order,
                        shop=shop,
                        number=product_number,
                        style="reserved",
                        price=product.price_sell,
                        day = ''
                    )
                    product_status_auto_change(product)
                return HttpResponse("OK!")
    else:
        shop = Shop.objects.get(code=shopCODE)
        products = Product.objects.all().filter(Q(shop=shop)&Q(web_cart=True))
        categories = set(products.values_list('category',flat=True))
        return render(request,'market/cart_index.html',{'shop':shop,'categories':categories})
    
