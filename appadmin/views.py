from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from db.models import *
from django.db.models import *
import datetime as dt 

def user_permission_auth(request):
    user = request.user
    try:
        user_admin = UserAdmin.objects.get(user=user)
        return ["allow",user_admin]
    except:
        return ["bad","dummy"]

@login_required
def dashboard(request):
    judge,user_data = user_permission_auth(request)
    shop = Shop.objects.all()
    if judge == "allow":
        return render(request,'admin/dashboard.html',{
            'shop':shop,
            'userconfig':user_data
        })
    else:
        return redirect('login')

@login_required
def news_post(request):
    judge,user_data = user_permission_auth(request)
    if judge == "allow":
        if request.method == "POST":
            return
        return render(request,'admin/news.html',{
            'userconfig':user_data
        })
    else:
        return redirect('login')

@login_required
def faq_post(request):
    judge,user_data = user_permission_auth(request)
    if judge == "allow":
        return render(request, 'admin/faq.html',{
            'userconfig':user_data
        })
    else:
        return redirect('login')

@login_required
def card(request):
    judge,user_data = user_permission_auth(request)
    if judge == "allow":
        return render(request, 'admin/faq.html',{
            'userconfig':user_data
        })
    else:
        return redirect('login')