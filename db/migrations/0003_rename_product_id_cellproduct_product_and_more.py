# Generated by Django 4.1.7 on 2023-07-23 21:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_alter_product_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cellproduct',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='shopID',
            new_name='shop',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='shopID',
            new_name='shop',
        ),
        migrations.RemoveField(
            model_name='cellproduct',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='cellproduct',
            name='ticket_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='Images',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_nameid',
        ),
        migrations.AddField(
            model_name='cellproduct',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cellproduct',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='db.order'),
        ),
        migrations.AddField(
            model_name='cellproduct',
            name='reason',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='cellproduct',
            name='style',
            field=models.CharField(default='import', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='ticket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='db.ticket'),
        ),
        migrations.AlterField(
            model_name='order',
            name='finished_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='finished_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
