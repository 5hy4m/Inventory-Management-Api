# Generated by Django 3.0.3 on 2020-02-11 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory_rest_api', '0013_productmodel_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customermodel',
            old_name='outstanding_recievables',
            new_name='recievables',
        ),
        migrations.AddField(
            model_name='vendormodel',
            name='payables',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='addressmodel',
            name='address_type',
            field=models.CharField(choices=[('customer', 'customer'), ('vendor', 'vendor'), ('organization', 'organization')], default='customer', max_length=20),
        ),
    ]
