# Generated by Django 4.1.7 on 2023-08-05 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0024_userdata_delete_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='market_active',
            field=models.BooleanField(default=False),
        ),
    ]