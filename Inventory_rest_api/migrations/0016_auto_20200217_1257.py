# Generated by Django 3.0.3 on 2020-02-17 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory_rest_api', '0015_billmodel_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitymodel',
            name='activity_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
