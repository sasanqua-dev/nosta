from django.urls import re_path , include , path
from django.contrib.auth import views as auth_views
from . import views

app_name ="appadmin"
urlpatterns = [
    path('console/dashboard', views.dashboard, name='dashboard'),
    path('console/news', views.news, name='news'),
    path('console/faq', views.faq, name='faq'),
]