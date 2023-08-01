# Generated by Django 4.1.7 on 2023-08-01 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0014_rename_regi_post_shop_webhock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(default='在庫なし', max_length=20),
            preserve_default=False,
        ),
    ]
