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
from module.user_auth import *
import random, string

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
            name=name,
            code=code,
            description = "",
            website="",
            message="",
            email_massege="",
            cstype="default",
            people_min=1,
            people_max=10,
            organization="",
            sic=sic,
            category=category,
            regi_ticket=False,
            is_active=True,
            token=randomstr(15)
        )
        VirtualUser.objects.create(
            user = request.user,
            shop = shop,
            permission = "owner",
            status = "approved",
        )
        return redirect('service',shop.code)

    else:
        return render(request, 'shop/register.html')

@login_required
def dashboard(request,shopCODE):
    if user_permission_auth(request,shopCODE,"editor") == "allow":
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
    if user_permission_auth(request,shopCODE,"editor") == "allow":
        shop = Shop.objects.get(code=shopCODE)
        return render(request, 'shop/console/analytics.html',{'shop':shop})
    else:
        return redirect('home')

@login_required
def members(request,shopCODE):
    if user_permission_auth(request,shopCODE,"editor") == "allow":
        shop = Shop.objects.get(code=shopCODE)
        vusers_approved = VirtualUser.objects.all().filter(shop=shop,status="approved")
        vusers_request = VirtualUser.objects.all().filter(shop=shop,status="request")
        return render(request, 'shop/console/member.html',{'shop':shop,'vusers_approved':vusers_approved,'vusers_request':vusers_request})
    else:
        return redirect('home')

@login_required
def settings(request,shopCODE):
    if user_permission_auth(request,shopCODE,"editor") == "allow":
        shop = Shop.objects.get(code=shopCODE)
        return render(request, 'shop/console/settings.html',{'shop':shop})
    else:
        return redirect('home')

@login_required
def profile(request,shopCODE):
    if user_permission_auth(request,shopCODE,"editor") == "allow":
        shop = Shop.objects.get(code=shopCODE)
        return render(request, 'shop/console/profile.html',{'shop':shop})
    else:
        return redirect('home')

@login_required
def market(request,shopCODE):
    if user_permission_auth(request,shopCODE,"editor") == "allow":
        shop = Shop.objects.get(code=shopCODE)
        return render(request, 'shop/console/market.html',{'shop':shop})
    else:
        return redirect('home')

@login_required
def product(request,shopCODE):
    if request.method == "POST":
        if user_permission_auth(request,shopCODE,"editor") == "allow":
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
                stock = CellProduct.objects.all().filter(Q(product=product)&Q(style="import")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"] - (CellProduct.objects.all().filter(Q(product=product)&Q(style="sold")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"] + CellProduct.objects.all().filter(Q(product=product)&Q(style="export")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"])
                all_import = CellProduct.objects.filter(Q(product=product)&Q(style="import")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"]
                if(all_import != 0): 
                    sales_rate = (CellProduct.objects.all().filter(Q(product=product)&Q(style="sold")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"] / all_import) * 100
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
                product.code = request.POST["code"]
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
                    code=request.POST["code"],
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
    if user_permission_auth(request,shopCODE,"editor") == "allow":
        shop = Shop.objects.get(code=shopCODE)
        categories = set(Product.objects.filter(shop=shop).values_list('category',flat=True))
        return render(request, 'shop/console/product.html',{'shop':shop,'categories':categories})
    else:
        return redirect('home')

@login_required
def order(request,shopCODE):
    if user_permission_auth(request,shopCODE,"editor") == "allow":
        if request.method == "POST":
            order = Order.objects.get(id=request.POST["id"])
            if request.POST["type"] == "get_detail":
                param = {
                    "order":order
                }
                data_detail = render_to_string("shop/console/order_detail_data.html",param)
                return HttpResponse(data_detail)
                
            elif request.POST["type"] == "get_order_products":
                products = CellProduct.objects.all().filter(order=order)
                param = {
                    "products":products
                }
                data_product = render_to_string("shop/console/order_product.html",param)
                return HttpResponse(data_product)
                
            elif request.POST["type"] == "post_order_treat":
                if request.POST["method"] == "delete":
                    Order.objects.get(id=request.POST["id"]).delete()
                elif request.POST["method"] == "return":
                    order = Order.objects.get(id=request.POST["id"])
                    order.status = "return"
                    order.save()
                    products = CellProduct.objects.all().filter(order=order)
                    for product in products:
                        product.price = 0
                        product.save()
                return HttpResponse("OK!")


        else:
            shop = Shop.objects.get(code=shopCODE)
            orders = Order.objects.all().filter(shop=shop)
            return render(request, 'shop/console/order.html',{'shop':shop,'orders':orders})
    else:
        return redirect('home')

def shopping(request,shopCODE):
    if request.method == "POST":
        shop = Shop.objects.get(code=shopCODE)
        match request.POST["type"]:
            case "get_product":
                products = Product.objects.all().filter(Q(shop=shop)&Q(category=request.POST["category"])&Q(web_cart=True))
                param = {
                    "products":products
                }
                data = render_to_string("shop/cart/product.html",param)
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
                data = HttpResponse(render_to_string('shop/cart/result.html',{'cart':cart,'shop':shop}))
                return HttpResponse(data)
    else:
        shop = Shop.objects.get(code=shopCODE)
        products = Product.objects.all().filter(Q(shop=shop)&Q(web_cart=True))
        categories = set(products.values_list('category',flat=True))
        return render(request,'shop/cart/index.html',{'shop':shop,'categories':categories})
    
