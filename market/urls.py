from django.urls import re_path , include , path
from . import views

app_name = "market"
urlpatterns = [
    path('<str:shopCODE>/', views.market, name='index'),
    #path('<str:shopCODE>/mypage', views.market, name='mypage'),
]