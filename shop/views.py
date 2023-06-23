from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from db.models import *
from django.db.models import *
import datetime as dt 
import pytz
import json

# Create your views here.
@login_required
def register(request):
    if request.method == 'POST':
        code = request.POST['shopcode']
        name = request.POST['shopname']
        sic = request.POST['sic']
        category = request.POST['category']
        if Shop.objects.filter(code = code).count() > 0:
            print(Shop.objects.filter(code = code).count())
            error_message = "この店舗コードはすでに使用されています(E005)"
            return render(request, 'shop/register.html', {'error': error_message})
        shop = Shop.objects.create(
            owner=request.user,
            name=name,
            code=code,
            description = "",
            website="",
            message="",
            cstype="default",
            people_min=1,
            people_max=10,
            organization="",
            sic=sic,
            category=category
        )
        return redirect('service',shop.code)

    else:
        return render(request, 'shop/register.html')

def get_dayformat():
    jst = pytz.timezone('Asia/Tokyo')
    now = dt.datetime.now(jst)
    formatted = str(now.strftime("%Y-%m-%d"))
    return formatted

def user_permission_auth(request,shopCODE):
    userdomain = request.user.email.split("@")[1]
    shop = Shop.objects.get(code=shopCODE)
    if(shop.owner == request.user) or ((shop.code in userdomain) and UserControl.objects.get(user=request.user).shopconsole == "valid"):
        return "allow"
    else:
        return "reject"
@login_required
def dashboard(request,shopCODE):
    if user_permission_auth(request,shopCODE) == "allow":
        shop = Shop.objects.get(code=shopCODE)
        formatted = get_dayformat()
        tickets_yet = Ticket.objects.all().filter(Q(status="Waiting")& Q(day=formatted)& Q(shopID=shop.id))
        tickets_calling = Ticket.objects.all().filter(Q(status="Calling")& Q(day=formatted)& Q(shopID=shop.id))
        orders_yet = Order.objects.all().filter(Q(status="Waiting")& Q(day=formatted)& Q(shopID=shop.id))
        orders_calling = Order.objects.all().filter(Q(status="Calling")& Q(day=formatted)& Q(shopID=shop.id))

        news = News.objects.all().filter(Q(channel="shop-console") | Q(channel="all")).order_by('created_at').reverse()[:5]
        # 来店者合計を計算
        result = Ticket.objects.filter(Q(day=formatted)&Q(shopID=shop)).aggregate(sum=models.Sum('people'))
        peoplesum = result["sum"]
        result = Ticket.objects.filter(Q(shopID=shop)).aggregate(sum=models.Sum('people'))
        allsum = result["sum"]

        return render(request, 'shop/console/dashboard.html',{
            'shop':shop,
            'news':news,
            'tickets_yet':tickets_yet,
            'tickets_calling':tickets_calling,
            'orders_waiting':orders_yet,
            'orders_calling':orders_calling,
            'peoplesum':peoplesum,
            'allsum':allsum,
        })
    else:
        return redirect('home')

@login_required
def analytics(request,shopCODE):
    if user_permission_auth(request,shopCODE) == "allow":
        shop = Shop.objects.get(code=shopCODE)
        return render(request, 'shop/console/analytics.html',{'shop':shop})
    else:
        return redirect('home')

@login_required
def members(request,shopCODE):
    if user_permission_auth(request,shopCODE) == "allow":
        shop = Shop.objects.get(code=shopCODE)
        return render(request, 'shop/console/member.html',{'shop':shop})
    else:
        return redirect('home')

@login_required
def settings(request,shopCODE):
    if user_permission_auth(request,shopCODE) == "allow":
        shop = Shop.objects.get(code=shopCODE)
        return render(request, 'shop/console/settings.html',{'shop':shop})
    else:
        return redirect('home')

@login_required
def profile(request,shopCODE):
    if user_permission_auth(request,shopCODE) == "allow":
        shop = Shop.objects.get(code=shopCODE)
        return render(request, 'shop/console/profile.html',{'shop':shop})
    else:
        return redirect('home')

@login_required
def market(request,shopCODE):
    if user_permission_auth(request,shopCODE) == "allow":
        shop = Shop.objects.get(code=shopCODE)
        return render(request, 'shop/console/market.html',{'shop':shop})
    else:
        return redirect('home')

@login_required
def product(request,shopCODE):
    if user_permission_auth(request,shopCODE) == "allow":
        shop = Shop.objects.get(code=shopCODE)
        return render(request, 'shop/console/product.html',{'shop':shop})
    else:
        return redirect('home')

@login_required
def order(request,shopCODE):
    if user_permission_auth(request,shopCODE) == "allow":
        shop = Shop.objects.get(code=shopCODE)
        return render(request, 'shop/console/order.html',{'shop':shop})
    else:
        return redirect('home')