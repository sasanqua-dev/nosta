from db.models import *
from django.db.models import *
from django.db.models.functions import Coalesce

def product_status_auto_change(product):
    stock = CellProduct.objects.all().filter(Q(product=product)&Q(style="import")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"] - (CellProduct.objects.all().filter(Q(product=product)&Q(style="sold")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"] + CellProduct.objects.all().filter(Q(product=product)&Q(style="export")).aggregate(total_count=Coalesce(models.Sum("number"),0))["total_count"])
    if stock > 10:
        product.status = "在庫あり"
    elif stock <= 10 and stock > 0:
        product.status = "残りわずか"
    else:
        product.status = "在庫なし"
    product.save()
    return