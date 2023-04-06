# Generated by Django 3.0 on 2021-02-21 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_delete_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catname', models.CharField(default='สินค้าทั่วไป', max_length=200)),
                ('detail', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('tel', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('detail', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='allproduct',
            name='fulldetail',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderpending',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='allproduct',
            name='catname',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Category'),
        ),
    ]