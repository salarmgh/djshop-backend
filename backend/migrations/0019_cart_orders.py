# Generated by Django 2.2.2 on 2019-08-15 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_remove_order_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='orders',
            field=models.ManyToManyField(related_name='cart', to='backend.Order'),
        ),
    ]
