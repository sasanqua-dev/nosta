# Generated by Django 4.1 on 2023-08-06 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0028_shopgrade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='secret',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='token',
            field=models.TextField(max_length=50),
        ),
    ]
