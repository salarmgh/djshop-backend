# Generated by Django 2.2.2 on 2019-08-15 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_auto_20190725_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
    ]
