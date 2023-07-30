from db.models import *
from django.db.models import *
from django.db.models.functions import Coalesce
import datetime as dt 
import pytz
import json

def user_permission_auth(request,shopCODE,permit):
    userdomain = request.user.email.split("@")[1]
    shop = Shop.objects.get(code=shopCODE)
    vuser = VirtualUser.objects.all().filter(shop=shop,user=request.user)
    if len(vuser) == 0:
        return "reject"
    if vuser[0].status == "approved":
        match vuser[0].permission:
            case "operator":
                if permit == "operator":
                    return "allow"
                else:
                    return "reject"
            case "editor":
                if permit == "operator":
                    return "allow"
                elif permit == "editor":
                    return "allow"
                else:
                    return "reject"
            case "admin":
                return "allow"
            case "owner":
                return "allow"
    else:
        return "reject"
    
def get_dayformat():
    jst = pytz.timezone('Asia/Tokyo')
    now = dt.datetime.now(jst)
    formatted = str(now.strftime("%Y-%m-%d"))
    return formatted

def randomstr(n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)