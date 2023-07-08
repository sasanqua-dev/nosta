# Generated by Django 4.1.7 on 2023-07-08 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='mail_massege',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shop',
            name='online_auth',
            field=models.CharField(default='false', max_length=10),
        ),
        migrations.AlterField(
            model_name='shop',
            name='message',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='shop',
            name='website',
            field=models.URLField(),
        ),
    ]