# Generated by Django 2.2.2 on 2019-08-16 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_cart_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
