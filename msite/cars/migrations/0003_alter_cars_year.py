# Generated by Django 4.0.4 on 2022-04-30 08:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_rename_brand_brands'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(2022)], verbose_name='Год выпуска'),
        ),
    ]
