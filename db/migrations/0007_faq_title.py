# Generated by Django 4.1.7 on 2023-06-22 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_alter_cellproduct_product_id_alter_cstype_shop_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='title',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]