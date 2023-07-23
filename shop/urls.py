from django.urls import re_path , include , path
from . import views

app_name = "shop"
urlpatterns = [
    path('register/', views.register, name='register'),
    path('console/dashboard/<str:shopCODE>', views.dashboard, name='dashboard'),
    path('console/analytics/<str:shopCODE>', views.analytics, name='analytics'),
    path('console/members/<str:shopCODE>', views.members, name='members'),
    path('console/settings/<str:shopCODE>', views.settings, name='settings'),
    path('console/profile/<str:shopCODE>', views.profile, name='profile'),
    path('console/market/<str:shopCODE>', views.market, name='market'),
    path('console/product/<str:shopCODE>', views.product, name='product'),
    path('console/product/ajax', views.product_ajax, name='product_ajax'),
    path('console/order/<str:shopCODE>', views.order, name='order'),
]