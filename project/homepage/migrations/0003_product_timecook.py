# Generated by Django 2.2.14 on 2021-12-11 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20211211_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='TimeCook',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
