# Generated by Django 2.2.2 on 2019-07-13 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20190706_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='کردنبند-cube'),
            preserve_default=False,
        ),
    ]