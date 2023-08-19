from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from db.models import *
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
def home(request):
    news = News.objects.all().filter(channel="all").order_by('created_at').reverse()
    return render(request,'about/top.html',{
        'news':news,
    })

def news(request):
    news = News.objects.all().order_by('created_at').reverse()
    return render(request,'about/news.html',{
        'news':news,
    })

def s_ticket(request):
    return render(request,'about/service/ticket.html',{
    })

def s_shop(request):
    return render(request,'about/service/shop.html',{
    })

def s_regi(request):
    return render(request,'about/service/regi.html',{
    })

def s_market(request):
    return render(request,'about/service/market.html',{
    })
def guide(request):
    return HttpResponse("準備中...")

def faq(request):
    general = FAQ.objects.all().filter(category="general")
    ticket = FAQ.objects.all().filter(category="ticket")
    shop = FAQ.objects.all().filter(category="shop")
    regi = FAQ.objects.all().filter(category="regi")
    market = FAQ.objects.all().filter(category="market")
    other = FAQ.objects.all().filter(category="other")
    return render(request,'about/support/faq.html',{
        'general':general,
        'ticket':ticket,
        'shop':shop,
        'regi':regi,
        'market':market,
        'other':other
    })

def about(request):
    return HttpResponse("準備中...")

def contact(request):
    if request.method == "POST":
        context = {
            "orgname":request.POST["org"],
            "username":request.POST["name"],
            "mail": request.POST["email"],
            "content": request.POST["content"]
        }
        subject = "お問い合わせいただきありがとうございます"
        message = strip_tags(render_to_string('mail/contact.html', context))
        from_email = "no-reply@nosta.prasic-plus.com"
        recipient_list =[request.POST["email"]]
        bcc = ["nostacs@gmail.com"]
        msg = EmailMessage(subject, message, from_email, recipient_list, bcc)
        msg.send()
        return render(request,'about/support/send.html')
    else:
        return render(request,'about/support/contact.html')

def terms(request):
    return render(request,'about/support/term.html')
    
def privacy(request):
    return render(request,'about/support/policy.html')