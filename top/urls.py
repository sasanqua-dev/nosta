from django.urls import re_path , include , path
from . import views

app_name = "top"
urlpatterns = [
    path('', views.home, name='home'),
]