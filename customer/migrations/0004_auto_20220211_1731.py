# Generated by Django 3.0.14 on 2022-02-11 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20220123_0755'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='fname',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='address',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='laname',
        ),
    ]
