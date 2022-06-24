# Generated by Django 4.0.4 on 2022-05-14 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cars', '0015_comments_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cars.cars', verbose_name='Автомобиль'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]