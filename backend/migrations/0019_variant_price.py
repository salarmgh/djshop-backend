# Generated by Django 2.2.2 on 2019-10-06 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_auto_20191006_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]