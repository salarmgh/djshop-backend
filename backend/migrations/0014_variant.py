# Generated by Django 2.2.2 on 2019-10-06 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_auto_20191006_0945'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('attribites', models.ManyToManyField(related_name='variants', to='backend.Attribute')),
                ('products', models.ManyToManyField(blank=True, related_name='variants', to='backend.Product')),
            ],
        ),
    ]