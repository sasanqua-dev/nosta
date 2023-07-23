from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from db.models import *
from django.db.models import *
from django.db.models.functions import Coalesce
import datetime as dt 
import pytz
import json
from django.template.loader import render_to_string

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
        tickets_yet = Ticket.objects.all().filter(Q(status="Waiting")& Q(day=formatted)& Q(shop=shop))
        tickets_calling = Ticket.objects.all().filter(Q(status="Calling")& Q(day=formatted)& Q(shop=shop))
        orders_yet = Order.objects.all().filter(Q(status="Waiting")& Q(day=formatted)& Q(shop=shop))
        orders_calling = Order.objects.all().filter(Q(status="Calling")& Q(day=formatted)& Q(shop=shop))

        news = News.objects.all().filter(Q(channel="shop-console") | Q(channel="all")).order_by('created_at').reverse()[:5]
        # 来店者合計を計算
        result = Ticket.objects.filter(Q(day=formatted)&Q(shop=shop)).aggregate(sum=models.Sum('people'))
        peoplesum = result["sum"]
        result = Ticket.objects.filter(Q(shop=shop)).aggregate(sum=models.Sum('people'))
        allsum = result["sum"]

        jst = pytz.timezone('Asia/Tokyo')
        now = dt.datetime.now(jst)
        earnings = CellProduct.objects.filter(Q(shop=shop)&Q(style="sold")&Q(day=get_dayformat())).aggregate(total_count=Coalesce(models.Sum("price"),0))["total_count"]

        return render(request, 'shop/console/dashboard.html',{
            'shop':shop,
            'news':news,
            'earnings':earnings,
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
    if request.method == "POST":
        if user_permission_auth(request,shopCODE) == "allow":
            shop = Shop.objects.get(code=shopCODE)
            if request.POST["type"] == "get_category":
                products = Product.objects.all().filter(Q(shop=shop)&Q(is_active=True)&Q(category=request.POST["category"]))
                param = {
                    "products": products,
                }
                data = render_to_string('shop/console/product_list.html', param)
                return HttpResponse(data)
            
            elif request.POST["type"] == "get_product":
                products = Product.objects.all().filter(Q(shop=shop)&Q(is_active=True))
                param = {
                    "products": products,
                }
                data = render_to_string('shop/console/product_list.html', param)
                return HttpResponse(data)
            
            elif request.POST["type"] == "get_product_sum":
                product = Product.objects.get(id=request.POST["id"])
                stock = CellProduct.objects.all().filter(product=product).aggregate(total_count=models.Sum("number"))["total_count"]
                all_import = CellProduct.objects.filter(Q(product=product)&Q(style="import")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"]
                if(all_import != 0): 
                    sales_rate = CellProduct.objects.all().filter(Q(product=product)&Q(style="sold")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"] / all_import
                    last_import = CellProduct.objects.all().filter(Q(product=product)&Q(style="import")).latest('id')
                else:
                    sales_rate = 0
                    last_import = None


                param = {
                    "stock": stock,
                    "sales_rate":sales_rate,
                    "last_import": last_import
                }
                data = render_to_string('shop/console/product_sales.html', param)
                return HttpResponse(data)

            elif request.POST["type"] == "post_product_edit":
                product = Product.objects.get(id=request.POST["id"])
                product.name = request.POST["name"]
                product.category = request.POST["category"]
                product.description = request.POST["description"]
                product.price_sell = request.POST["price_sell"]
                product.price_buy = request.POST["price_buy"]
                product.save()
                return HttpResponse("OK")
            
            elif request.POST["type"] == "post_product_new":
                Product.objects.create(
                    shop=shop,
                    name=request.POST["name"],
                    category=request.POST["category"],
                    price_sell=request.POST["price_sell"],
                    price_buy=request.POST["price_buy"],
                    description=request.POST["description"],
                    is_active=True
                )
                return HttpResponse("OK")

            elif request.POST["type"] == "post_product_delete":
                product = Product.objects.get(id=request.POST["id"])
                product.delete()
                return HttpResponse("OK")
            
            elif request.POST["type"] == "post_product_stock":
                product = Product.objects.get(id=request.POST["id"])
                if (request.POST["price"] == "") and (request.POST["style"] == "import"):
                    price = product.price_buy * int(request.POST["number"])
                elif (request.POST["price"] == "") and (request.POST["style"] == "export"):
                    price = 0
                else:
                    price = request.POST["price"]
                
                CellProduct.objects.create(
                    product=product,
                    shop=shop,
                    number=request.POST["number"],
                    style=request.POST["style"],
                    price=price,
                    day=get_dayformat()
                )
                return HttpResponse("OK")
        else:
            return HttpResponse("Permission Error")
    if user_permission_auth(request,shopCODE) == "allow":
        shop = Shop.objects.get(code=shopCODE)
        categories = Product.objects.filter(shop=shop).values_list('category',flat=True)
        return render(request, 'shop/console/product.html',{'shop':shop,'categories':categories})
    else:
        return redirect('home')

@login_required
def order(request,shopCODE):
    if user_permission_auth(request,shopCODE) == "allow":
        shop = Shop.objects.get(code=shopCODE)
        return render(request, 'shop/console/order.html',{'shop':shop})
    else:
        return redirect('home')