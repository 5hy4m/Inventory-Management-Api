# Generated by Django 2.2.5 on 2019-10-19 04:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerModel',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=30)),
                ('address', models.TextField()),
                ('phone_no', models.BigIntegerField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=50)),
                ('product_description', models.TextField(max_length=200)),
                ('category', models.CharField(choices=[('VideoGames', 'videogames'), ('ActionFigures', 'actionfigures'), ('Vintage', 'vintage'), ('books', 'books'), ('electronics', 'electronics'), ('adapter', 'adapter')], default='VideoGames', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StockModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('location', models.TextField()),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Inventory_rest_api.ProductModel')),
            ],
        ),
        migrations.CreateModel(
            name='SellModel',
            fields=[
                ('sell_id', models.AutoField(primary_key=True, serialize=False)),
                ('selling_price', models.FloatField()),
                ('sell_date', models.DateField()),
                ('quantity', models.IntegerField()),
                ('customer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Inventory_rest_api.CustomerModel')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Inventory_rest_api.ProductModel')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='Inventory_rest_api.ProductModel')),
            ],
        ),
        migrations.CreateModel(
            name='BuyModel',
            fields=[
                ('buy_id', models.AutoField(primary_key=True, serialize=False)),
                ('buy_date', models.DateField()),
                ('quantity', models.IntegerField()),
                ('cost_price', models.IntegerField()),
                ('customer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Inventory_rest_api.CustomerModel')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Inventory_rest_api.ProductModel')),
            ],
        ),
    ]