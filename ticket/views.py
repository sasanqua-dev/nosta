from django.shortcuts import render, redirect , reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from db.models import *
from django.db.models import *
import datetime as dt 
import pytz
import json

from module.user_auth import *

def consolo_access(request,shopCODE,authtype=None):
    shop = Shop.objects.get(code=shopCODE)
    if authtype:
        if user_permission_auth(request,shopCODE,"editor") == "allow":
            return True,shop
        else:
            return False,"dummy"
    if user_permission_auth(request,shopCODE,"editor") == "allow": 
        formatted = get_dayformat()
        tickets = Ticket.objects.all().filter(Q(shop=shop) & Q(day=formatted)& Q(shop=shop)).count()
        tickets_already = Ticket.objects.all().filter((Q(status="Canceled") | Q(status="Skipped")| Q(status="Called"))& Q(day=formatted)& Q(shop=shop))
        tickets_calling = Ticket.objects.all().filter(Q(status="Calling") & Q(day=formatted)& Q(shop=shop))
        tickets_yet = Ticket.objects.all().filter(Q(status="Waiting")& Q(day=formatted)& Q(shop=shop))
        return shop,tickets,tickets_already,tickets_calling,tickets_yet,formatted
    else:
        return "bad","dummy","dummy","dummy","dummy","dummy"


@login_required
def dashboard(request,shopCODE):
    shop,tickets,tickets_already,tickets_calling,tickets_yet,formatted = consolo_access(request,shopCODE)
    if shop == "bad":
        return redirect('ticket:home')

    news = News.objects.all().filter(Q(channel="ticket-console") | Q(channel="all")).order_by('created_at').reverse()[:3]
    # 来店者合計を計算
    result = Ticket.objects.filter(Q(day=formatted)&Q(shop=shop)).aggregate(sum=models.Sum('people'))
    peoplesum = result["sum"]
    result = Ticket.objects.filter(Q(shop=shop)).aggregate(sum=models.Sum('people'))
    allsum = result["sum"]
    return render(request, 'ticket/console/dashboard.html',{
        'shop':shop,
        'news':news,
        'tickets':tickets,
        'tickets_already':tickets_already,
        'tickets_calling':tickets_calling,
        'tickets_yet':tickets_yet,
        'peoplesum':peoplesum,
        'allsum':allsum,
        'tickets_callingAndalready':tickets_calling.count() + tickets_already.count()
    })

@login_required
def customers(request,shopCODE):
    shop,tickets,tickets_already,tickets_calling,tickets_yet,formatted = consolo_access(request,shopCODE)
    return render(request, 'ticket/console/customers.html',{
        'shop':shop,
        'tickets':tickets,
        'tickets_already':tickets_already,
        'tickets_yet':tickets_yet,
        'tickets_calling':tickets_calling
    })

@login_required
def shop(request,shopCODE):
    shop = Shop.objects.get(code=shopCODE)
    if user_permission_auth(request,shopCODE,"editor") == "allow":
        cstype_list = CStype.objects.all().filter(shop=shop)
        return render(request, 'ticket/console/shop.html',{'shop':shop,'cstype_list':cstype_list})
    else:
        return redirect('home')


@login_required
def reception_internal(request,shopCODE):
    shop = Shop.objects.get(code=shopCODE)
    cstype_list = CStype.objects.all().filter(shop=shop)
    if user_permission_auth(request,shopCODE,"operator") == "allow":
        return render(request, 'ticket/reception.html',{'shop':shop,'cstype_list':cstype_list})
    else:
        return redirect('home')

@csrf_exempt
def system_ajax(request):
    match request.POST["command"]:
        case 'create_tickets':
            formatted = get_dayformat()
            shop = Shop.objects.get(id=request.POST["shopID"])
            latestnumber = Ticket.objects.all().filter(Q(shop = shop) & Q(day=formatted)).aggregate(Max('number'))["number__max"]
            Ticket.objects.all().filter(Q(shop = shop) & Q(day=formatted))
            if latestnumber == None:
                latestnumber = 0
            ticket = Ticket.objects.create(
                number=latestnumber + 1,
                shop=shop,
                people=request.POST["people"],
                cstype=request.POST["cstype"],
                status="Waiting",
                location=request.POST["provider"],
                day=str(formatted),
                waiting=0
            )
            data = {
                "ticket_number":ticket.number,
                "ticket_created":str(ticket.created_at.strftime("%Y/%m/%d %H:%M:%S"))
            }
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            return HttpResponse(json_str)
        
        case 'called_ticket':
            tid = request.POST["tid"]
            jst = pytz.timezone('Asia/Tokyo')
            now = dt.datetime.now(jst)
            ticket = Ticket.objects.get(id=tid)
            ticket.status = "Called"
            ticket.finished_at = now
            ticket.save()
            return HttpResponse("OK!")
        
        case 'calling_ticket':
            tid = request.POST["tid"]
            ticket = Ticket.objects.get(id=tid)
            ticket.status = "Calling"
            ticket.save()
            return HttpResponse("OK!")

        case 'skipped_ticket':
            tid = request.POST["tid"]
            jst = pytz.timezone('Asia/Tokyo')
            now = dt.datetime.now(jst)
            ticket = Ticket.objects.get(id=tid)
            ticket.status = "Skipped"
            ticket.finished_at = now
            ticket.save()
            return HttpResponse("OK!")

        case 'canceled_ticket':
            tid = request.POST["tid"]
            jst = pytz.timezone('Asia/Tokyo')
            now = dt.datetime.now(jst)
            ticket = Ticket.objects.get(id=tid)
            ticket.status = "Canceled"
            ticket.finished_at = now
            ticket.save()
            return HttpResponse("OK!")
    
        case 'setting':
            tf,shop = consolo_access(request,request.POST["shopcode"],"AUTH")
            if tf == True:
                shop.name = request.POST["shop_name"]
                shop.message = request.POST["shop_message"]
                shop.people_min = request.POST["min_number"]
                shop.people_max = request.POST["max_number"]
                #shop.online_ticket = request.POST["reception_online"]
                #shop.online_auth = request.POST["userauth"]
                shop.email_message = request.POST["email_message"]
                shop.save()
                return HttpResponse("OK!")

            else:
                return

def customerview(request,shopCODE):
    shop = Shop.objects.get(code=shopCODE)
    dayformat = get_dayformat()
    tickets_calling = Ticket.objects.all().filter(Q(status="Calling") & Q(day=dayformat)& Q(shop=shop))
    return render(request,'ticket/customer/all_view.html',{'shop':shop,'tickets_calling':tickets_calling})

def shopview(request,shopCODE):
    shop = Shop.objects.get(code=shopCODE)
    dayformat = get_dayformat()
    tickets_calling = Ticket.objects.all().filter(Q(status="Calling") & Q(day=dayformat)& Q(shop=shop))
    tickets_waiting = Ticket.objects.all().filter(Q(status="Waiting") & Q(day=dayformat)& Q(shop=shop))
    return render(request,'ticket/customer/shop_view.html',{'shop':shop,'tickets_calling':tickets_calling,'tickets_waiting':tickets_waiting})