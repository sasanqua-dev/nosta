# Generated by Django 4.1.7 on 2023-06-22 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0007_faq_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='faq',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]