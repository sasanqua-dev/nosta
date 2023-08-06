# Generated by Django 4.1 on 2023-08-06 03:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('db', '0001_initial'), ('db', '0002_alter_product_images'), ('db', '0003_rename_product_id_cellproduct_product_and_more'), ('db', '0004_cellproduct_shop'), ('db', '0005_cellproduct_day'), ('db', '0006_rename_mail_massege_shop_email_massege'), ('db', '0007_shop_regi_ticket_alter_shop_is_active'), ('db', '0008_order_cs_price_order_number_order_remaining_price_and_more'), ('db', '0009_shop_regi_post'), ('db', '0010_product_code_alter_product_description'), ('db', '0011_virtualuser_remove_usercontrol_user_and_more'), ('db', '0012_remove_virtualuser_is_active_shop_token_and_more'), ('db', '0013_shop_secret'), ('db', '0014_rename_regi_post_shop_webhock'), ('db', '0015_product_images_product_status'), ('db', '0016_rename_images_product_image'), ('db', '0017_order_email_product_limit_shop_order_limit_and_more'), ('db', '0018_remove_shop_message_shop_ucc_baner_shop_ucc_resource_and_more'), ('db', '0019_alter_shop_description_alter_shop_email_massege_and_more'), ('db', '0020_alter_product_limit_alter_shop_ucc_baner_and_more'), ('db', '0021_order_customer_ticket_customer'), ('db', '0022_product_cancel_vadminuser'), ('db', '0023_review_resource_customuser_cellresource'), ('db', '0024_userdata_delete_customuser'), ('db', '0025_shop_market_active'), ('db', '0026_alter_product_limit'), ('db', '0027_shop_regi_post'), ('db', '0028_shopgrade'), ('db', '0029_alter_order_secret_alter_shop_token')]

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orgname', models.CharField(max_length=100)),
                ('usrname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('status', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(default='Lite', max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('website', models.URLField(null=True)),
                ('email_massege', models.CharField(max_length=1000, null=True)),
                ('people_min', models.IntegerField(null=True)),
                ('people_max', models.IntegerField(null=True)),
                ('online_ticket', models.CharField(default='false', max_length=10)),
                ('online_auth', models.CharField(default='false', max_length=10)),
                ('sic', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('organization', models.CharField(max_length=1000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField()),
                ('regi_ticket', models.BooleanField(default=True)),
                ('webhock', models.URLField(blank=True)),
                ('token', models.TextField(max_length=50)),
                ('secret', models.CharField(default='asdfafs', max_length=50)),
                ('order_limit', models.IntegerField(null=True)),
                ('regi_pass', models.BooleanField(default=False)),
                ('ucc_baner', models.TextField(default='', max_length=2000, null=True)),
                ('ucc_resource', models.TextField(default='', max_length=2000, null=True)),
                ('ucc_ticket', models.TextField(default='', max_length=2000, null=True)),
                ('ucc_treasure', models.TextField(default='', max_length=2000, null=True)),
                ('market_active', models.BooleanField(default=False)),
                ('regi_post', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('people', models.IntegerField()),
                ('cstype', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=50)),
                ('day', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('finished_at', models.DateTimeField(auto_now=True)),
                ('waiting', models.IntegerField()),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.shop')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=20)),
                ('price_sell', models.IntegerField()),
                ('price_buy', models.IntegerField()),
                ('description', models.TextField(null=True)),
                ('is_active', models.BooleanField()),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.shop')),
                ('code', models.CharField(max_length=20, null=True)),
                ('web_cart', models.BooleanField(default=False)),
                ('image', models.URLField(null=True)),
                ('status', models.CharField(default='在庫なし', max_length=20)),
                ('limit', models.IntegerField(default=5)),
                ('cancel', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('day', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('finished_at', models.DateTimeField(auto_now=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.shop')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='db.ticket')),
                ('cs_price', models.IntegerField(default=0)),
                ('number', models.IntegerField(default=0)),
                ('remaining_price', models.IntegerField(default=0)),
                ('total_price', models.IntegerField(default=0)),
                ('reserved_date', models.DateTimeField(null=True)),
                ('reserved_id', models.IntegerField(null=True)),
                ('secret', models.CharField(max_length=1000, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('tag', models.CharField(max_length=100)),
                ('channel', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CStype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.shop')),
            ],
        ),
        migrations.CreateModel(
            name='CellProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('price', models.IntegerField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.product')),
                ('created_at', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='db.order')),
                ('reason', models.TextField(max_length=1000, null=True)),
                ('style', models.CharField(default='import', max_length=10)),
                ('shop', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='db.shop')),
                ('day', models.CharField(default='2023-07-24', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='VirtualUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(max_length=10, null=True)),
                ('status', models.CharField(max_length=10, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('team', models.CharField(max_length=50, null=True)),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='db.shop')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.virtualuser'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='VadminUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=50, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('permission', models.CharField(max_length=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('content', models.TextField(default='')),
                ('status', models.CharField(default='normal', max_length=10)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.shop')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('people', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('memo', models.TextField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.shop')),
            ],
        ),
        migrations.CreateModel(
            name='CellResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='using', max_length=10)),
                ('memo', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='db.order')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.resource')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='db.virtualuser')),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorites', models.ManyToManyField(related_name='favorites', to='db.shop')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShopGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=10)),
                ('expire_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='db.shop')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='secret',
            field=models.CharField(max_length=200, null=True),
        ),
    ]