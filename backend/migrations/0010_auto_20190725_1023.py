# Generated by Django 2.2.2 on 2019-07-25 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_order_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cover',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]