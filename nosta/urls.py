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
    path('admin/', admin.site.urls),
    #path('', include('top.urls')),
    path('shop/', include('shop.urls')),
    path('app/', include('userapp.urls')),
    path('market/', include('market.urls')),
    path('regi/', include('regi.urls')),
    path('ticket/', include('ticket.urls')),
    path('auth/', include('appauth.urls')),
    path('news/',include('news.urls')),
    path('', include('top.urls')),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
