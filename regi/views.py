from django.shortcuts import render, redirect , reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from db.models import *
from django.db.models import *
from django.db.models.functions import Coalesce
import datetime as dt 
import pytz
import json
import hashlib

from module.api_sold import *
from module.user_auth import *
from module.product_status import *

@login_required
def index(request,shopCODE):
    if request.method == "POST":
        if user_permission_auth(request,shopCODE,"operator") == "allow":
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
                if request.POST["ticket"] == "" or int(request.POST["ticket"]) == 0:
                    ticket_data = None
                else:
                    ticket_data = Ticket.objects.get(id=request.POST["ticket"])

                user = VirtualUser.objects.all().filter(shop=shop,user=request.user)[0]
                order = Order.objects.create(
                    user = user,
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
                    product_status_auto_change(product)
                
                if shop.regi_post != False:
                    api_send(shop,order)

                return HttpResponse("OK!")
            
            elif request.POST["type"] == "get_list":
                orders = Order.objects.all().filter(Q(shop=shop)&Q(status="complete"))
                param = {
                    "orders": orders,
                }
                data = render_to_string('regi/parts/order_list.html', param)
                return HttpResponse(data)
            
        else:
            return HttpResponse("Permission Error")
    if user_permission_auth(request,shopCODE,"operator") == "allow":
        shop = Shop.objects.get(code=shopCODE)
        vuser = VirtualUser.objects.filter(Q(shop=shop)&Q(user=request.user))[0]
        categories = sorted(set(Product.objects.filter(shop=shop).values_list('category',flat=True)))
        return render(request, 'regi/base.html',{'shop':shop,"categories":categories,'vuser':vuser})
    else:
        return redirect('home')

def order_auth(code,shop):
    body = code.split(':')[1]
    oid = body.split('/')[0]
    hsecret = body.split('/')[1]
    if not Order.objects.all().filter(Q(id=oid)&Q(shop=shop)).exists():
        return "order:incorrect"
    order = Order.objects.get(id=oid)
    if hashlib.sha224(order.secret.encode()).hexdigest() != hsecret:
        return "secret:incorrect"

    else:
        return "allow"

@login_required
def app(request,shopCODE):
        if user_permission_auth(request,shopCODE,"operator") == "allow":
            if request.method == "POST":
                shop = Shop.objects.get(code=shopCODE)
                match request.POST["type"]:
                    case "change_state":
                        oid = request.POST["id"]
                        state = request.POST["state"]
                        order = Order.objects.get(id=oid)
                        order.status = state
                        if state == "complete":
                            order.cs_price = request.POST['recieved']
                            order.remaining_price = request.POST['return']
                            order.day = get_dayformat()
                        order.user = VirtualUser.objects.filter(Q(user=request.user)&Q(shop=shop))[0]
                        order.save()
                        return HttpResponse("OK!")

                    case "get_code":
                        code = request.POST["code"]
                        if "ticket" in code:
                            return HttpResponse(render_to_string('regi/app/unsupport.html',{}))
                        elif "order" in code:
                            body = code.split(':')[1]
                            oid = body.split('/')[0]
                            if order_auth(code,shop) == "allow":
                                order = Order.objects.get(id=oid)
                                products = CellProduct.objects.all().filter(order=order)
                                param = {
                                    'order':order,
                                    'products':products
                                }
                                data = render_to_string('regi/app/orderdetail.html',param)
                                return HttpResponse(data)
                            
                            else:
                                param = {
                                    'message':order_auth(code,shop)
                                }
                                data = render_to_string('regi/app/orderdetail.html',param)
                                return HttpResponse(data)

                        else:
                            day = get_dayformat()
                            products = Product.objects.all().filter(Q(shop=shop)&Q(code=code))
                            if products.count() == 0:
                                return HttpResponse(render_to_string('regi/app/unsupport.html',{}))
                            products_sold = []
                            products_stock = []
                            for product in products:
                                stock = CellProduct.objects.all().filter(Q(product=product)&Q(style="import")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"] - (CellProduct.objects.all().filter(Q(product=product)&Q(style="sold")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"] + CellProduct.objects.all().filter(Q(product=product)&Q(style="export")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"])
                                sold = CellProduct.objects.all().filter(Q(product=product)&Q(style="sold")&Q(day=day)).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"]
                                temp_stock = {
                                    "name" : product.name,
                                    "category" : product.category,
                                    "stock" : stock
                                }
                                products_stock.append(temp_stock)
                                temp_sold = {
                                    "name" : product.name,
                                    "category" : product.category,
                                    "sold" : sold
                                }
                                products_sold.append(temp_sold)

                            param = {
                                'products_object':products,
                                'products_sold':products_sold,
                                'products_stock':products_stock
                            }
                            data = render_to_string('regi/app/products.html', param)
                            return HttpResponse(data)
                    case "action":
                        sub_command = request.POST["sub_command"]
                        code = request.POST["code"]
                        body = code.split(':')[1]
                        id = body.split('/')[0]
                        if "order" in code:
                            if order_auth(code,shop) == "allow":
                                if sub_command == "create_ticket":
                                    order = Order.objects.get(reserved_id=id)
                                    latestnumber = Ticket.objects.all().filter(Q(shop = shop) & Q(day=formatted)).aggregate(Max('number'))["number__max"]
                                    if latestnumber == None:
                                        latestnumber = 0
                                    ticket = Ticket.objects.create(
                                        number=latestnumber+1,
                                        shop=order.shop,
                                        people=request.POST["people"],
                                        cstype=request.POST["cstype"],
                                        localtion="reserved",
                                        status="waiting",
                                        day=get_dayformat(),
                                        waiting=0
                                    )
                                    order.ticket = ticket
                                    order.save()
                                    param = {
                                        'shop':shop,
                                        'ticket':ticket,
                                        'order':order
                                    }
                                    data = render_to_string('regi/app/orderdetail.html',param)
                                    return HttpResponse(data)
                            
                            else:
                                param = {
                                    'message':order_auth(code,shop)
                                }
                                data = render_to_string('regi/app/orderdetail.html',param)
                                return HttpResponse(data)

                    case _:
                        return HttpResponse(render_to_string('regi/app/unsupport.html',{}))
            else:
                shop = Shop.objects.get(code=shopCODE)
                return render(request,'regi/app.html',{'shop':shop})
        else:
            return redirect('home')