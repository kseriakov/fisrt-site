# Generated by Django 4.0.4 on 2022-04-29 14:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=50, verbose_name='Наименование бренда')),
            ],
            options={
                'verbose_name': 'Автомобильный бренд',
                'verbose_name_plural': 'Автомобильные бренды',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=50, verbose_name='Марка')),
                ('year', models.IntegerField(validators=[django.core.validators.MaxLengthValidator(2022)], verbose_name='Год выпуска')),
                ('engine_capacity', models.FloatField(verbose_name='Объем двигателя')),
                ('engine_power', models.IntegerField(verbose_name='Мощность двигателя')),
                ('type_of_engine', models.CharField(choices=[(None, 'Выберите тип двигателя'), ('petrol', 'Бензиновый'), ('diesel', 'Дизельный')], db_index=True, max_length=50, verbose_name='Тип двигателя')),
                ('transmission', models.CharField(choices=[(None, 'Выберите тип коробки передач'), ('automatic', 'Автоматическая коробка передач'), ('manual', 'Механическая коробка передач')], db_index=True, max_length=50, verbose_name='Коробка передач')),
                ('drive', models.CharField(choices=[(None, 'Выберите тип привода'), ('all', 'Полный привод'), ('front', 'Передний привод'), ('rear', 'Задний привод')], db_index=True, max_length=50, verbose_name='Привод')),
                ('image', models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('content', models.TextField(db_index=True, verbose_name='Описание авто')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cars.brand', verbose_name='Бренд')),
            ],
            options={
                'verbose_name': 'Автомобиль',
                'verbose_name_plural': 'Автомобили',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, verbose_name='Комментарии')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cars.cars', verbose_name='Автомобиль')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]