from django.db import models
from django.contrib.auth import get_user, get_user_model
User = get_user_model()

# Create your models here.

class Shop(models.Model):
    # フィールドの定義
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.CharField(max_length=100,default="Lite")
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    website = models.CharField(max_length=1000)
    message = models.CharField(max_length=1000)

    people_min = models.IntegerField()
    people_max = models.IntegerField()

    online_ticket = models.CharField(max_length=10,default="false")
    
    sic = models.CharField(max_length=50)
    category = models.CharField(max_length=50)

    organization = models.CharField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.CharField(max_length=50)

    def __str__(self):
        return self.code  # モデルの文字列表現
    
class Ticket(models.Model):
    # フィールドの定義
    number = models.IntegerField()
    shopID = models.ForeignKey(Shop, on_delete=models.CASCADE)

    people = models.IntegerField()
    cstype = models.CharField(max_length=100)
    location = models.CharField(max_length=1000)

    status = models.CharField(max_length=50)
    day = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now_add=True)
    waiting = models.IntegerField()

    def __str__(self):
        return str(self.number)  # モデルの文字列表現
    

class Product(models.Model):
    product_nameid = models.CharField(max_length=100)
    shopID = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price_sell = models.IntegerField()
    price_buy = models.IntegerField()
    description = models.CharField(max_length=1000)
    Images = models.ImageField(upload_to='')
    is_active = models.CharField(max_length=50)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shopID = models.ForeignKey(Shop, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now_add=True)

class CellProduct(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    number = models.IntegerField()
    price = models.IntegerField()

class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    channel = models.CharField(max_length=100)
    message = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CStype(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)