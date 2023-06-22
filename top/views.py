from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from db.models import *

# Create your views here.
def home(request):
    news_important = News.objects.all().filter(channel="important").order_by('created_at').reverse()
    news_info = News.objects.all().filter(channel="info").order_by('created_at').reverse()
    return render(request,'top/top.html',{
        'news_important':news_important,
        'news_info':news_info
    })

def s_ticket(request):
    return HttpResponse("準備中...")

def s_shop(request):
    return HttpResponse("準備中...")

def s_regi(request):
    return HttpResponse("準備中...")

def s_market(request):
    return HttpResponse("準備中...")

def guide(request):
    return HttpResponse("準備中...")

def faq(request):
    return HttpResponse("準備中...")

def about(request):
    return HttpResponse("準備中...")

def contact(request):
    return HttpResponse("準備中...")

def terms(request):
    return render(request,'top/support/terms.html')
    
def policy(request):
    return render(request,'top/support/policy.html')