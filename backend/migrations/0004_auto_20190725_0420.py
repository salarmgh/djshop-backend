# Generated by Django 2.2.2 on 2019-07-25 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20190725_0404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
        migrations.AddField(
            model_name='order',
            name='attribute',
            field=models.ManyToManyField(related_name='order_attributes', to='backend.ProductAttribute'),
        ),
        migrations.DeleteModel(
            name='OrderAttribute',
        ),
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='orders_cart', to='backend.Cart'),
            preserve_default=False,
        ),
    ]
