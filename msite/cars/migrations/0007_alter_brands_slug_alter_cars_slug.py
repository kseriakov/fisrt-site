# Generated by Django 4.0.4 on 2022-05-03 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0006_brands_slug_cars_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brands',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='cars',
            name='slug',
            field=models.SlugField(blank=True, default='get_slug', verbose_name='URL'),
        ),
    ]
