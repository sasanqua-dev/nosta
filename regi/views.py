from django.shortcuts import render, redirect , reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from db.models import *
from django.db.models import *
import datetime as dt 
import pytz
import json

def user_permission_auth(request,shopCODE):
    userdomain = request.user.email.split("@")[1]
    shop = Shop.objects.get(code=shopCODE)
    if(shop.owner == request.user) or ((shop.code in userdomain) and UserControl.objects.get(user=request.user).shopconsole == "valid"):
        return "allow"
    else:
        return "reject"

def get_dayformat():
    jst = pytz.timezone('Asia/Tokyo')
    now = dt.datetime.now(jst)
    formatted = str(now.strftime("%Y-%m-%d"))
    return formatted

@login_required
def index(request,shopCODE):
    if request.method == "POST":
        if user_permission_auth(request,shopCODE) == "allow":
            shop = Shop.objects.get(code=shopCODE)
            if request.POST["type"] == "get_ticket_waiting":
                formatted = get_dayformat()
                tickets = Ticket.objects.all().filter(Q(status="Waiting")& Q(day=formatted)& Q(shop=shop))
                param = {
                    'tickets':tickets,
                }
                data = render_to_string('regi/parts/customer.html', param)
                return HttpResponse(data)
            
            elif request.POST["type"] == "get_ticket_calling":
                formatted = get_dayformat()
                tickets = Ticket.objects.all().filter(Q(status="Calling")& Q(day=formatted)& Q(shop=shop))
                param = {
                    'tickets':tickets,
                }
                data = render_to_string('regi/parts/customer.html', param)
                return HttpResponse(data)
        
            elif request.POST["type"] == "get_category":
                products = Product.objects.all().filter(Q(shop=shop)&Q(is_active=True)&Q(category=request.POST["category"]))
                param = {
                    "products": products,
                }
                data = render_to_string('regi/parts/product_cell.html', param)
                return HttpResponse(data)
            
            elif request.POST["type"] == "get_product":
                products = Product.objects.all().filter(Q(shop=shop)&Q(is_active=True))
                param = {
                    "products": products,
                }
                data = render_to_string('regi/parts/product_cell.html', param)
                return HttpResponse(data)
            
            elif request.POST["type"] == "post_treasurer":
                shop = Shop.objects.get(code=shopCODE)
                if(shop.regi_ticket):
                    status = "recived"
                else:
                    status = "complete"
                if request.POST["ticket"] == "":
                    ticket_data = None
                else:
                    ticket_data = Ticket.objects.get(id=request.POST["ticket"])

                order = Order.objects.create(
                    user = request.user,
                    shop = Shop.objects.get(code=shopCODE),
                    status = status,
                    day = get_dayformat(),
                    ticket = ticket_data,
                    total_price = request.POST["total_price"],
                    cs_price = request.POST["cs_price"],
                    remaining_price = request.POST["remaining_price"],
                    number = request.POST["number"],
                )
                for product_id,product_number in zip(json.loads(request.POST["products_ids"]),json.loads(request.POST["products_numbers"])):
                    product = Product.objects.get(id=product_id)
                    CellProduct.objects.create(
                        product=product,
                        order=order,
                        shop=shop,
                        number=product_number,
                        style="sold",
                        price=product.price_sell,
                        day = get_dayformat()
                    )
                return HttpResponse("OK!")
            
            elif request.POST["type"] == "get_list":
                orders = Order.objects.all().filter(shop=shop)
                param = {
                    "orders": orders,
                }
                data = render_to_string('regi/parts/order_list.html', param)
                return HttpResponse(data)
            
        else:
            return HttpResponse("Permission Error")
    if user_permission_auth(request,shopCODE) == "allow":
        shop = Shop.objects.get(code=shopCODE)
        categories = sorted(set(Product.objects.filter(shop=shop).values_list('category',flat=True)))
        return render(request, 'regi/base.html',{'shop':shop,"categories":categories})
    else:
        return redirect('home')