# Generated by Django 2.2.2 on 2019-10-20 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_product_attributes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variant',
            name='attributes',
            field=models.ManyToManyField(blank=True, related_name='variants', to='backend.Attribute'),
        ),
    ]
