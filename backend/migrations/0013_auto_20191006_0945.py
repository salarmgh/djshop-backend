# Generated by Django 2.2.2 on 2019-10-06 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_auto_20191006_0944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='attributes',
        ),
    ]