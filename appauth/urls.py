from django.urls import re_path , include , path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    re_path(r'^login/', views.user_login, name='login'),
    re_path(r'^logout/', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^register/', views.user_register, name='register'),
    re_path(r'^social-auth/', include('social_django.urls', namespace='social')),
    path('service/<str:shopCODE>', views.service, name='service'),
    path('', views.home, name='home')
]