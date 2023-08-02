from django.shortcuts import render, redirect , reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from db.models import *
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        userid = request.POST['userid']
        password = request.POST['password']
        user = authenticate(request, username=userid, password=password)
        if user is not None:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect(request.GET["next"]) # ログイン後にリダイレクトするURLを指定します
        else:
            # ログイン失敗時の処理
            return render(request, 'auth/login.html', {'error': 'ユーザーIDまたはパスワードが間違っています(E001)'})
    else:
        return render(request, 'auth/login.html')

def user_register(request):
    if request.method == 'POST':
        userid = request.POST['userid']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if User.objects.filter(email = userid).count() > 0:
            error_message = "このメールアドレスはすでに登録されています(E002)"
            return render(request, 'auth/register.html', {'error': error_message})
        if '.nosta' in userid:
            error_message = "このメールアドレスは使用できません(E003)"
            return render(request, 'auth/register.html', {'error': error_message})
        if User.objects.filter(username = username).count() > 0:
            error_message = "このユーザー名はすでに登録されています(E004)"
            return render(request, 'auth/register.html', {'error': error_message})
        if password != password2 :
            error_message = "パスワードが一致しません(E005)"
            return render(request, 'auth/register.html', {'error': error_message})
        user = User.objects.create_user(
            username=username,
            email=userid,
            password=password,
            is_active="True"
            )

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect('home')

    else:
        return render(request, 'auth/register.html')

@login_required
def service(request,shopCODE):
    return render(request,'auth/service.html',{'shop':shopCODE})

@login_required
def home(request):
    message = ''
    if request.method == "POST":
        shop_code = request.POST["code"]
        shop_token = request.POST["token"]
        if not Shop.objects.all().filter(code=shop_code).exists():
            message = "不正な店舗コードです"
            vusers = VirtualUser.objects.all().filter(user=request.user)
            return render(request, 'auth/home.html',{'vusers':vusers,"message":message})
        if VirtualUser.objects.all().filter(shop=shop,user=request.user).count() > 1:
            message = "この店舗へはすでに登録されています"
            vusers = VirtualUser.objects.all().filter(user=request.user)
            return render(request, 'auth/home.html',{'vusers':vusers,"message":message})

        if shop == None:
            message = "店舗コードが間違っています"
            vusers = VirtualUser.objects.all().filter(user=request.user)
            return render(request, 'auth/home.html',{'vusers':vusers,"message":message})
        if shop.secret == shop_token :
            VirtualUser.objects.create(
                user = request.user,
                shop = shop,
                name= request.POST["name"],
                status = "request"
            )
            return redirect('home')
        else:
            message = "認証トークンが間違っています"
            vusers = VirtualUser.objects.all().filter(user=request.user)
            return render(request, 'auth/home.html',{'vusers':vusers,"message":message})

    userid = request.user.id
    vusers = VirtualUser.objects.all().filter(user=request.user)
    return render(request, 'auth/home.html',{'vusers':vusers,"message":message})
