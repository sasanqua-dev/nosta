from django.urls import re_path , include , path
from . import views

app_name = "shop"
urlpatterns = [
    path('home/<int:shopCODE>', views.home, name='home'),
    path('register/', views.register, name='register'),

    path('console/dashboard/<int:shopCODE>', views.dashboard, name='dashboard'),
    path('console/analytics/<int:shopCODE>', views.analytics, name='analytics'),
    path('console/members/<int:shopCODE>', views.members, name='members'),
    path('console/settings/<int:shopCODE>', views.settings, name='settings'),
    path('console/profile/<int:shopCODE>', views.profile, name='profile'),
    path('console/market/<int:shopCODE>', views.market, name='market'),
    path('console/product/<int:shopCODE>', views.product, name='product'),
    path('console/order/<int:shopCODE>', views.order, name='order'),
]