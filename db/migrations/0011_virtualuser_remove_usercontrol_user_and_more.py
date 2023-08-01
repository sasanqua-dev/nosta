# Generated by Django 4.1.7 on 2023-07-31 00:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('db', '0010_product_code_alter_product_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(max_length=10, null=True)),
                ('status', models.CharField(max_length=10, null=True)),
                ('is_active', models.CharField(max_length=50, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('team', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='usercontrol',
            name='user',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='owner',
        ),
        migrations.AddField(
            model_name='order',
            name='reserved_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='reserved_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='secret',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='web_cart',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='UserAdmin',
        ),
        migrations.DeleteModel(
            name='UserControl',
        ),
        migrations.AddField(
            model_name='virtualuser',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='db.shop'),
        ),
        migrations.AddField(
            model_name='virtualuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
