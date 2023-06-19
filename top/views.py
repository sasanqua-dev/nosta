from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from db.models import *

# Create your views here.
@login_required
def home(request):
    return HttpResponse("Hello World")