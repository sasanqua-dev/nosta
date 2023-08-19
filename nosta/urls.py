"""nosta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from django.contrib.auth import views as auth_views
from django.views.static import serve 
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_control

urlpatterns = [
    path('system/admin/', admin.site.urls),
    path('', include('top.urls')),
    path('shop/', include('shop.urls')),
    path('app/', include('userapp.urls')),
    path('market/', include('market.urls')),
    path('regi/', include('regi.urls')),
    path('ticket/', include('ticket.urls')),
    path('auth/', include('appauth.urls')),
    path('news/',include('news.urls')),
    path('about/', include('about.urls')),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    path('accounts/password_change_form/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change_form'),
    path('accounts/password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_finish.html'), name='password_change_done'),
    path('accounts/password_reset_form/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),    # 追加
    path('accounts/password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_mail_done.html'), name='password_reset_done'),    # 追加
    path('accounts/password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirmation.html'), name='password_reset_confirm'),    # 追加
    path('accounts/password_reset_finish/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_finish.html'), name='password_reset_complete'),    # 追加
]
