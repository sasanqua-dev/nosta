from django.urls import re_path , include , path
from django.contrib.auth import views as auth_views
from . import views

app_name ="ticket"
urlpatterns = [
    path('console/dashboard/<str:shopCODE>', views.dashboard, name='dashboard'),
    path('console/customers/<str:shopCODE>', views.customers, name='customers'),
    path('console/settings/<str:shopCODE>', views.shop, name='shop'),
    path('view/<str:shopCODE>', views.customerview, name='client_external'),
    path('view/internal/<str:shopCODE>', views.shopview, name='client_internal'),
    path('reception/internal/<str:shopCODE>', views.reception_internal, name='reception_internal'),
    path('system/ajax',views.system_ajax,name='ajax')
]