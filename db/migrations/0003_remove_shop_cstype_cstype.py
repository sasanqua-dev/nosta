# Generated by Django 4.2.2 on 2023-06-20 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_news'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='cstype',
        ),
        migrations.CreateModel(
            name='CStype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.shop')),
            ],
        ),
    ]
