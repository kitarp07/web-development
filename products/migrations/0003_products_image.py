# Generated by Django 3.0.14 on 2022-01-25 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20220125_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]