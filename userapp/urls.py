from django.urls import re_path , include , path
from . import views

app_name = "userapp"
urlpatterns = [
    path('', views.index, name='index'),
]