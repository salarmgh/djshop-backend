# Generated by Django 2.2.2 on 2019-07-25 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_auto_20190725_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]