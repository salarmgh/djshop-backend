# Generated by Django 2.2.2 on 2019-10-06 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0021_auto_20191006_1729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='products',
        ),
    ]
