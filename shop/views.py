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
from module.product_status import *
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
            sic=sic,
            category=category,
            regi_ticket=False,
            is_active=True,
            token=randomstr(60),
            secret=randomstr(10)
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

        webproducts = Product.objects.all().filter(shop=shop,web_cart=True).count()
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
            'webproducts':webproducts
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
    if request.method == "POST":
        if user_permission_auth(request,shopCODE,"editor") == "allow":
            shop = Shop.objects.get(code=shopCODE)
            vuser = VirtualUser.objects.get(id=request.POST["id"])
            current_vuser = VirtualUser.objects.all().filter(shop=shop,user=request.user)[0]
            match request.POST["command"]:
                case "change_user_status":
                    vuser.status = request.POST["status"]
                    vuser.save()
                    return HttpResponse("OK!")
            
                case "update_user_profile":
                    if current_vuser.permission == "admin" or current_vuser.permission == "owner" :
                        vuser.permission = request.POST["permission"]
                        vuser.status = request.POST["status"]
                    vuser.name = request.POST["name"]
                    vuser.team = request.POST["team"]
                    vuser.save()
                    return HttpResponse("OK!")
                
                case "get_user_profile":
                    shop = Shop.objects.get(code=shopCODE)
                    param = {
                        "cuser":current_vuser,
                        "vuser":vuser,
                        'shop':shop
                    }
                    data = render_to_string("shop/console/member_vuser_detail.html",param)
                    return HttpResponse(data)
                
                case "delete_virtual_user":
                    vuser = VirtualUser.objects.get(id=request.POST["id"])
                    vuser.delete()
                    return HttpResponse("OK!")

    else:
        if user_permission_auth(request,shopCODE,"editor") == "allow":
            shop = Shop.objects.get(code=shopCODE)
            vusers_approved = VirtualUser.objects.all().filter(shop=shop,status="approved")
            vusers_request = VirtualUser.objects.all().filter(shop=shop,status="request")
            current_vuser = VirtualUser.objects.all().filter(shop=shop,user=request.user)[0]
            return render(request, 'shop/console/member.html',{'shop':shop,'vusers_approved':vusers_approved,'vusers_request':vusers_request,'cuser':current_vuser})
        else:
            return redirect('home')

@login_required
def settings(request,shopCODE):
    if user_permission_auth(request,shopCODE,"editor") == "allow":
        shop = Shop.objects.get(code=shopCODE)
        if request.method == "POST":
            match request.POST["command"]:
                case "settings":
                    def tagblocker(st):
                        st = st.replace('<script>','')
                        st = st.replace('<link','')
                        return st
                    shop.name = request.POST["name"]
                    shop.website = request.POST["url"]
                    shop.description = request.POST["description"]
                    shop.regi_pass = request.POST["regi_pass"]
                    shop.ucc_baner = tagblocker(request.POST["ucc_baner"])
                    shop.ucc_treasure = tagblocker(request.POST["ucc_treasure"])
                    shop.ucc_ticket = tagblocker(request.POST["ucc_ticket"])
                    shop.ucc_resource = tagblocker(request.POST["ucc_resource"])
                    shop.webhock = request.POST["webhock"]
                    shop.save()
                    return HttpResponse("OK!")
                case "re_gererate":
                    if request.POST["type"] == "secret":
                        secret = randomstr(10)
                        shop.secret = secret
                        shop.save()
                        return HttpResponse(secret)
                    elif request.POST["type"] == "token":
                        token = randomstr(60)
                        shop.token = token
                        shop.save()
                        return HttpResponse(token)
        else:
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
        products = Product.objects.all().filter(shop=shop,web_cart=True)
        return render(request, 'shop/console/market.html',{'shop':shop,'products':products})
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
            
            elif request.POST["type"] == "get_category_list":
                categories = set(Product.objects.filter(shop=shop).values_list('category',flat=True))
                param = {
                    "categories": categories,
                }
                data = render_to_string('shop/console/product_category.html', param)
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
                reserved = CellProduct.objects.all().filter(Q(product=product)&Q(style="reserved")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"]
                stock = CellProduct.objects.all().filter(Q(product=product)&Q(style="import")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"] - (CellProduct.objects.all().filter(Q(product=product)&Q(style="sold")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"] + CellProduct.objects.all().filter(Q(product=product)&Q(style="export")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"])
                all_import = CellProduct.objects.filter(Q(product=product)&Q(style="import")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"]
                sold = CellProduct.objects.all().filter(Q(product=product)&Q(style="sold")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"]
                export = CellProduct.objects.all().filter(Q(product=product)&Q(style="export")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"]
                if(all_import != 0): 
                    sales_rate = ((sold + export) / all_import) * 100
                    sales_rate_pre = (( sold + reserved + export) / all_import) * 100
                    last_import = CellProduct.objects.all().filter(Q(product=product)&Q(style="import")).latest('id')
                else:
                    sales_rate = 0
                    sales_rate_pre = 0
                    last_import = None


                param = {
                    "stock": stock,
                    "reserved": reserved,
                    "sales_rate":round(sales_rate,2),
                    "sales_rate_pre":round(sales_rate_pre,2),
                    "last_import": last_import,
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
                product.web_cart = request.POST["web_cart"]
                product.image = request.POST["image"]
                product.limit = request.POST["limit"]
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
                    web_cart=request.POST["web_cart"],
                    image=request.POST["image"],
                    limit=request.POST["limit"],
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
                product_status_auto_change(product)
                return HttpResponse("OK!")
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
                elif request.POST["method"] == "complete":
                    order = Order.objects.get(id=request.POST["id"])
                    order.day = get_dayformat()
                    order.status = "complete"
                    order.save()
                return HttpResponse("OK!")


        else:
            shop = Shop.objects.get(code=shopCODE)
            complete_orders = Order.objects.all().filter(shop=shop,status="complete")
            return_orders = Order.objects.all().filter(shop=shop,status="return")
            reserved_orders = Order.objects.all().filter(shop=shop,status="reserved")
            return render(request, 'shop/console/order.html',{
                'shop':shop,
                'complete_orders':complete_orders,
                'return_orders':return_orders,
                'reserved_orders':reserved_orders
            })
    else:
        return redirect('home')