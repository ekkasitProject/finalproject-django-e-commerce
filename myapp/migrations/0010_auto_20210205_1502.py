# Generated by Django 3.0 on 2021-02-05 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_orderlist_orderpending'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpending',
            name='other',
            field=models.TextField(blank=True, null=True),
        ),
    ]