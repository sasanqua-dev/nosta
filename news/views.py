from django.shortcuts import render
from db.models import *

# Create your views here.
def detail(request,id):
    news = News.objects.get(id=id)
    return render(request,'news/detail.html',{
        'news':news
        })
