from django.shortcuts import render,redirect
from django.http import HttpResponse
from db.models import *
from django.db.models import *
from django.db.models.functions import *
from django.template.loader import render_to_string

# Create your views here.
def top(requests):
    shops = Shop.objects.filter(market_active=True).annotate(fav=Count('favorites')).order_by('fav')
    return render(requests,'top/index.html',{'shops':shops})
def search(requests):
    key = requests.POST["key"]
    shops = Shop.objects.filter(Q(market_active=True)&(Q(name__icontains=key)|Q(description__icontains=key))).annotate(fav=Count('favorites')).order_by('fav')
    data = render_to_string('top/search.html',{
        'shops':shops
    })
    return HttpResponse(data)