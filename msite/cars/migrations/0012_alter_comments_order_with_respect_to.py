# Generated by Django 4.0.4 on 2022-05-07 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0011_remove_cars_pre_slug'),
    ]

    operations = [
        migrations.AlterOrderWithRespectTo(
            name='comments',
            order_with_respect_to='car',
        ),
    ]
