# Generated by Django 4.1.7 on 2023-08-02 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0017_order_email_product_limit_shop_order_limit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='message',
        ),
        migrations.AddField(
            model_name='shop',
            name='ucc_baner',
            field=models.TextField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='ucc_resource',
            field=models.TextField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='ucc_ticket',
            field=models.TextField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='ucc_treasure',
            field=models.TextField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.virtualuser'),
        ),
    ]
