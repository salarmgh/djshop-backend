# Generated by Django 2.2.2 on 2019-07-25 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattributevalue',
            name='products',
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(related_name='order_products', to='backend.Product'),
        ),
        migrations.CreateModel(
            name='OrderAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('product', models.ManyToManyField(related_name='order_attribute_products', to='backend.Product')),
            ],
        ),
    ]