from django.urls import re_path , include , path
from . import views

app_name = "top"
urlpatterns = [
    path('', views.home, name='home'),
    path('service/ticket', views.s_ticket, name='se_ticket'),
    path('service/shop', views.s_shop, name='se_shop'),
    path('service/regi', views.s_regi, name='se_regi'),
    path('service/market', views.s_market, name='se_market'),
    path('support/guide', views.guide, name='guide'),
    path('support/contact', views.contact, name='contact'),
    path('support/faq', views.faq, name='faq'),
    path('support/about', views.about, name='about'),
    path('document/terms', views.terms, name='terms'),
    path('document/privacy', views.privacy, name='privacy'),
]