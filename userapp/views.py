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
from datetime import datetime

from module.api_sold import *
from module.user_auth import *
from module.product_status import *

import hashlib

@login_required
def index(request):
    if request.method == "POST":
        match request.POST["type"]:
            case "post_change_user_data":
                user_data = User.objects.get(email=request.user.email)
                user_data.email = request.POST["email"]
                user_data.first_name = request.POST["first_name"]
                user_data.last_name = request.POST["last_name"]
                user_data.save()
                return HttpResponse("OK!")
                
            case "post_delete_user_data":
                now_tickets = Ticket.objects.all().filter(Q(customer=request.user)&Q(Q(status="Waiting")|Q(status="Calling")))
                orders = Order.objects.all().filter(Q(customer=request.user)&Q(status="reserved"))
                if (now_tickets.count() == 0 & orders.count() == 0):
                    request.user.delete()
                    redirect('logout')
                else:
                    return HttpResponse("OK!")
                
            case "get_detail":
                order = Order.objects.get(id=request.POST["id"])
                products = CellProduct.objects.all().filter(order=order)
                param = {
                    'order': order,
                    'products':products,
                    'order_secret': hashlib.sha224(order.secret.encode()).hexdigest()
                }
                data = render_to_string('userapp/parts/orderdetail.html',param)
                return HttpResponse(data)
            
            case "cancel":
                order = Order.objects.get(id=request.POST["id"])
                products = CellProduct.objects.all().filter(order=order)
                for pdc in products:
                    if pdc.cancel == True:
                        pass
                    elif pdc.cancel == False:
                        return HttpResponse("error")
                        
                order.status = "cancel"
                order.save()
                products.update(number=0)
                products.update(price=0)
                return HttpResponse("OK!")
    else:
        now_tickets = Ticket.objects.all().filter(Q(customer=request.user)&Q(Q(status="Waiting")|Q(status="Calling")))
        tickets = Ticket.objects.all().filter(Q(customer=request.user)&Q(status="reserved"))
        orders = Order.objects.all().filter(Q(customer=request.user)&Q(status="reserved"))
        today = datetime.now()
        hour = today.hour
        # 時間帯によりメッセージを変えて表示
        if hour >= 3 and hour <= 9:
            message = "おはようございます！"
        elif hour >= 10 and hour <=21:
            message = "こんにちは！"
        else:
            message = "こんばんは！"
        if VadminUser.objects.all().filter(user=request.user).exists():
            va_user = VadminUser.objects.all().filter(user=request.user)[0]
        else:
            va_user = None
        
        try:
            provider = request.user.social_auth.first().provider
        except:
            provider = None
        param = {
            'va_user':va_user,
            'message':message,
            'provider':provider,
            'now_tickets':tickets,
            'tickets':tickets,
            'orders':orders,
            'user_secret':hashlib.sha224(str(request.user.email).encode()).hexdigest()
        }
        return render(request,'userapp/index.html',param)