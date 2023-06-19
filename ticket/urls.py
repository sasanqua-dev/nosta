from django.urls import re_path , include , path
from django.contrib.auth import views as auth_views
from . import views

app_name ="ticket"
urlpatterns = [
    path('', views.home, name='home'),
    path('console/dashboard/<int:shopID>', views.dashboard, name='dashboard'),
    path('console/customers/<int:shopID>', views.customers, name='customers'),
    path('console/settings/<int:shopID>', views.shop, name='shop'),
    path('view/<int:shopID>', views.customerview, name='client_external'),
    path('view/internal/<int:shopID>', views.shopview, name='client_internal'),
    path('reception/internal/<int:shopID>', views.reception_internal, name='reception_internal'),
    path('system/ajax',views.system_ajax,name='ajax')
]