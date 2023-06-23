from django.urls import re_path , include , path
from django.contrib.auth import views as auth_views
from . import views

app_name ="news"
urlpatterns = [
    path('detail/<int:id>', views.detail, name='detail'),
]