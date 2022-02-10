# Generated by Django 3.0.14 on 2022-01-23 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='fname',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='laname',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='password',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='customer',
            name='username',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]