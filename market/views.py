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

# Create your views here.
def market(request,shopCODE):
    if request.method == "POST":
        shop = Shop.objects.get(code=shopCODE)
        match request.POST["type"]:
            case "get_products":
                products = Product.objects.all().filter(Q(shop=shop)&Q(web_cart=True))
                param = {
                    "products":products
                }
                data = render_to_string("market/cart/products.html",param)
                return HttpResponse(data)
            case "set_cart":
                if request.POST["ticket_create"] == False:
                    ticket = None
                else:
                    formatted = get_dayformat()
                    latestnumber = Ticket.objects.all().filter(Q(shop = shop) & Q(day=formatted)).aggregate(Max('number'))["number__max"]
                    if latestnumber == None:
                        latestnumber = 0
                    ticket = Ticket.objects.create(
                        number=latestnumber+1,
                        shop=shop,
                        people=1,
                        cstype=None,
                        localtion="WebCart",
                        status="Waiting",
                        waiting=0
                    )
                cart = Cart.objects.create(
                    shop=shop,
                    products=request.POST["products"],
                    ticket=ticket,
                )
                data = HttpResponse(render_to_string('market/cart/result.html',{'cart':cart,'shop':shop}))
                return HttpResponse(data)
    else:
        shop = Shop.objects.get(code=shopCODE)
        products = Product.objects.all().filter(Q(shop=shop)&Q(web_cart=True))
        categories = set(products.values_list('category',flat=True))
        return render(request,'market/cart_index.html',{'shop':shop,'categories':categories})
    
