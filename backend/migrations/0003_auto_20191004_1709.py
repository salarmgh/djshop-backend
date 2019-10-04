# Generated by Django 2.2.2 on 2019-10-04 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20191004_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carousel',
            name='image',
            field=models.ImageField(upload_to='images/carousel/'),
        ),
        migrations.AlterField(
            model_name='category',
            name='cover',
            field=models.ImageField(blank=True, default='', upload_to='images/categories/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images/products/'),
        ),
    ]
