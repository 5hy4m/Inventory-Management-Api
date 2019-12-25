# Generated by Django 2.2.5 on 2019-12-25 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory_rest_api', '0008_auto_20191225_0804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockmodel',
            name='id',
        ),
        migrations.AlterField(
            model_name='stockmodel',
            name='commited',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='stockmodel',
            name='product_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Inventory_rest_api.ProductModel'),
        ),
    ]