# Generated by Django 2.2.2 on 2019-07-25 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_auto_20190725_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
