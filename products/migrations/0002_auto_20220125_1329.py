# Generated by Django 3.0.14 on 2022-01-25 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Customer',
            new_name='Products',
        ),
    ]