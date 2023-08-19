from django.urls import re_path , include , path
from . import views

app_name = "top"
urlpatterns = [
    path('', views.top, name='index'),
    ## Search is not view but also api.
    path('/search',views.search,name="search")
]