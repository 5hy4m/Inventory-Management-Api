# Generated by Django 3.0.3 on 2020-02-23 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory_rest_api', '0017_auto_20200221_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='billmodel',
            name='subtotal',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='billmodel',
            name='total',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='invoicemodel',
            name='subtotal',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='invoicemodel',
            name='total',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='purchaseordermodel',
            name='subtotal',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='purchaseordermodel',
            name='total',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='salesordermodel',
            name='subtotal',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='salesordermodel',
            name='total',
            field=models.FloatField(default=0),
        ),
    ]
