from django.urls import re_path , include , path
from . import views

app_name = "regi"
urlpatterns = [
    path('<str:shopCODE>', views.index, name='index'),
]