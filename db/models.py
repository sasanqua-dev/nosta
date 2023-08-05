from django.db import models
from django.contrib.auth.models import *
from django.contrib.auth import get_user, get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
User = get_user_model()

# Create your models here.

class Shop(models.Model):
    # フィールドの定義
    grade = models.CharField(max_length=100,default="Lite")
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    description = models.TextField(null=True)

    
    website = models.URLField(null=True)

    email_massege = models.CharField(max_length=1000,null=True)

    people_min = models.IntegerField(null=True)
    people_max = models.IntegerField(null=True)

    online_ticket = models.CharField(max_length=10,default="false")
    online_auth = models.CharField(max_length=10,default="false")
    
    sic = models.CharField(max_length=50)
    category = models.CharField(max_length=50)

    organization = models.CharField(max_length=1000,null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    regi_ticket = models.BooleanField(default=True)
    regi_pass = models.BooleanField(default=False)
    regi_post = models.BooleanField(default=False)
    market_active = models.BooleanField(default=False)
    webhock = models.URLField(blank=True)

    secret = models.CharField(max_length=50)
    token = models.CharField(max_length=50)

    order_limit = models.IntegerField(null=True)
    
    ucc_baner = models.TextField(null=True,max_length=2000,default="")
    ucc_treasure = models.TextField(null=True,max_length=2000,default="")
    ucc_ticket = models.TextField(null=True,max_length=2000,default="")
    ucc_resource = models.TextField(null=True,max_length=2000,default="")

    is_active = models.BooleanField()

    def __str__(self):
        return self.name

class ShopGrade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,null=True)
    code = models.CharField(max_length=50)
    status = models.CharField(max_length=10)
    expire_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    star = models.IntegerField(default=3,validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField(default="")
    status = models.CharField(default="normal",max_length=10)

class UserData(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Shop,related_name="favorites")

class VirtualUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,null=True)
    permission = models.CharField(max_length=10,null=True)
    status = models.CharField(max_length=10,null=True)
    name = models.CharField(max_length=50,null=True)
    team = models.CharField(max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class VadminUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.CharField(max_length=50,null=True)
    name = models.CharField(max_length=50,null=True)
    permission = models.CharField(max_length=10,null=True)
    def __str__(self):
        return self.name

class CStype(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

class Ticket(models.Model):
    # フィールドの定義
    customer = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    number = models.IntegerField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    cstype = models.ForeignKey(CStype, on_delete=models.SET_NULL,null=True)
    people = models.IntegerField()
    cstype = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    day = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now=True)
    waiting = models.IntegerField()
    def __str__(self):
        return str(self.number)  # モデルの文字列表現

class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20)
    price_sell = models.IntegerField()
    price_buy = models.IntegerField()
    description = models.TextField(null=True)
    code = models.CharField(max_length=20,null=True)
    web_cart = models.BooleanField(default=False)
    image = models.URLField(null=True)
    status = models.CharField(max_length=20)
    limit = models.IntegerField(default=5)
    cancel = models.BooleanField(default=True)
    is_active = models.BooleanField()
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(VirtualUser, on_delete=models.SET_NULL,null=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    day = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE,null=True)
    number = models.IntegerField()
    total_price = models.IntegerField()
    cs_price = models.IntegerField()
    remaining_price = models.IntegerField()

    reserved_date =  models.DateTimeField(null=True)
    secret = models.CharField(max_length=1000,null=True)
    reserved_id = models.IntegerField(null=True)
    email = models.EmailField(null=True)

class CellProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    number = models.IntegerField()
    style = models.CharField(max_length=10)
    reason = models.TextField(max_length=1000,null=True)
    price = models.IntegerField()
    day = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

class Resource(models.Model):
    code = models.CharField(max_length=50)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE)
    people = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    memo = models.TextField(null=True)
    is_active = models.BooleanField(default=True)

class CellResource(models.Model):
    resource = models.ForeignKey(Resource,on_delete=models.CASCADE)
    status = models.CharField(default="using",max_length=10)
    user = models.ForeignKey(VirtualUser,on_delete=models.CASCADE,null=True)
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    memo = models.TextField(null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    channel = models.CharField(max_length=100)
    message = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title



class FAQ(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Contact(models.Model):
    orgname = models.CharField(max_length=100)
    usrname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    content = models.TextField()
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.usrname
