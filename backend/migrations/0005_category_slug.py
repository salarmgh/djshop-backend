# Generated by Django 2.2.2 on 2019-07-13 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='گردنبند'),
            preserve_default=False,
        ),
    ]
