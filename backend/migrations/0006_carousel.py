# Generated by Django 2.2.2 on 2019-07-13 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_category_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('url', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
