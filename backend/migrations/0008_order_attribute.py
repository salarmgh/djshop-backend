# Generated by Django 2.2.2 on 2019-07-25 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_remove_order_attribute'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='attribute',
            field=models.ManyToManyField(related_name='order_attributes', to='backend.ProductAttributeValue'),
        ),
    ]