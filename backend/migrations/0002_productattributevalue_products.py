# Generated by Django 2.2.2 on 2019-07-03 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattributevalue',
            name='products',
            field=models.ManyToManyField(related_name='attribute_values', to='backend.Product'),
        ),
    ]
