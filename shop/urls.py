from django.urls import re_path , include , path
from . import views

app_name = "shop"
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
]