from django.shortcuts import render, redirect , reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from db.models import *

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        userid = request.POST['userid']
        password = request.POST['password']
        user = authenticate(request, email=userid, password=password)
        if user is not None:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('shop:home') # ログイン後にリダイレクトするURLを指定します
        else:
            # ログイン失敗時の処理
            return render(request, 'login.html', {'error': 'ユーザーIDまたはパスワードが間違っています(E001)'})
    else:
        return render(request, 'auth/login.html')

def user_register(request):
    if request.method == 'POST':
        userid = request.POST['userid']
        username = request.POST['username']
        password = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password2 = request.POST['password2']
        if User.objects.filter(email = userid).count() > 0:
            error_message = "このメールアドレスはすでに登録されています(E002)"
            return render(request, 'register.html', {'error': error_message})
        if '.nicket' in userid:
            error_message = "このメールアドレスは使用できません(E003)"
            return render(request, 'register.html', {'error': error_message})
        if User.objects.filter(username = username).count() > 0:
            error_message = "このユーザー名はすでに登録されています(E004)"
            return render(request, 'register.html', {'error': error_message})
        if password != password2 :
            error_message = "パスワードが一致しません(E005)"
            return render(request, 'register.html', {'error': error_message})
        user = User.objects.create_user(
            username=username,
            email=userid,
            password=password,
            firstname=firstname,
            lastname=lastname,
            grade="Free",
            is_active="active"
            )

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect('shop:home')

    else:
        return render(request, 'auth/register.html')