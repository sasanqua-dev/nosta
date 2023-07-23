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
        else:
            return HttpResponse("Permission Error")
    if user_permission_auth(request,shopCODE) == "allow":
        shop = Shop.objects.get(code=shopCODE)
        return render(request, 'regi/base.html',{'shop':shop})
    else:
        return redirect('home')