from django.urls import re_path , include , path
from . import views

app_name = "shop"
urlpatterns = [
    path('home/<int: shopID>', views.home, name='home'),
    path('register/', views.register, name='register'),

    path('console/dashboard/<int:shopID>', views.dashboard, name='dashboard'),
    path('console/analytics/<int:shopID>', views.analytics, name='analytics'),
    path('console/members/<int:shopID>', views.members, name='members'),
    path('console/settings/<int:shopID>', views.settings, name='settings'),
    path('console/profile/<int:shopID>', views.profile, name='profile'),
    path('console/market/<int:shopID>', views.market, name='market'),
    path('console/product/<int:shopID>', views.product, name='product'),
    path('console/order/<int:shopID>', views.order, name='order'),
]