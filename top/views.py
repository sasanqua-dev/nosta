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