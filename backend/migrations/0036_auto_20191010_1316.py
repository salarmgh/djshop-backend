# Generated by Django 2.2.2 on 2019-10-10 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0035_auto_20191010_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variant',
            name='image',
            field=models.ManyToManyField(blank=True, related_name='variants', to='backend.Image'),
        ),
    ]
