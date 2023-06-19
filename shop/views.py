from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from db.models import *

# Create your views here.
@login_required
def home(request):
    return HttpResponse("Hello World")

@login_required
def dashboard(request,shopID):
    return HttpResponse("this is console")

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
        return redirect('shop:home')

    else:
        return render(request, 'shop/register.html')