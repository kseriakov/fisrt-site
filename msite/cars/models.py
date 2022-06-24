from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, IntegrityError
from django.http import Http404, HttpResponseServerError
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save

from .for_signals import *

import re
from transliterate import slugify, translit
from langdetect import detect


class Cars(models.Model):

    DRIVE_CHOICES = [
        (None, 'Выберите тип привода'),
        ('all', 'Полный привод'),
        ('front', 'Передний привод'),
        ('rear', 'Задний привод')
    ]

    TRANSMISSION_CHOICES = [
        (None, 'Выберите тип коробки передач'),
        ('automatic', 'Автоматическая коробка передач'),
        ('manual', 'Механическая коробка передач'),
    ]

    TYPE_OF_ENGINE = [
        (None, 'Выберите тип двигателя'),
        ('petrol', 'Бензиновый'),
        ('diesel', 'Дизельный')
    ]

    brand = models.ForeignKey('Brands', on_delete=models.PROTECT, verbose_name='Бренд', db_index=True)
    title = models.CharField(max_length=50, verbose_name='Марка', db_index=True)
    year = models.IntegerField(validators=[MaxValueValidator(3000), MinValueValidator(1900)], verbose_name='Год выпуска')
    engine_capacity = models.FloatField(verbose_name='Объем двигателя', validators=[MinValueValidator(0), MaxValueValidator(15)])
    engine_power = models.IntegerField(verbose_name='Мощность, л/с')
    type_of_engine = models.CharField(max_length=50, verbose_name='Двигатель', db_index=True, choices=TYPE_OF_ENGINE)
    transmission = models.CharField(max_length=50, verbose_name='Коробка передач', db_index=True, choices=TRANSMISSION_CHOICES)
    drive = models.CharField(max_length=50, verbose_name='Привод', db_index=True, choices=DRIVE_CHOICES)
    image = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    content = models.TextField(verbose_name='Описание авто', db_index=True)
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True, blank=True, null=True)

    @staticmethod
    def get_translit(word):
        trnslt = translit(word, language_code='ru', reversed=True)
        return trnslt

    # Формируем slug
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            raise Http404

        if not self.slug:
            self.slug = slugify(f'{self.get_translit(self.brand.title)} {self.get_translit(self.title)} {self.pk}', 'el')
            self.save(*args, **kwargs)

    def __str__(self):
        return f'{self.brand} {self.title}'

    class Meta:
        verbose_name = 'Автомобиль'  # Имя приложения
        verbose_name_plural = 'Автомобили'  # Имя приложения во множественном числе
        ordering = ['-create_at']  # Сортировка записей

        # Ограничения на поля
        constraints = (
            models.CheckConstraint(check=models.Q(year__gte=1900) & models.Q(year__lte=3000),
                                            name='%(app_label)s_%(class)s_year_constraint'),
            models.CheckConstraint(check=models.Q(engine_capacity__gt=0) & models.Q(engine_capacity__lt=15),
                                   name='%(app_label)s_%(class)s_engine_capacity_constraint'),
        )

    def get_absolute_url(self):
        return reverse('view_car', kwargs={'slug_car': self.slug})


class Brands(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name='Наименование бренда')
    slug = models.SlugField(db_index=True, verbose_name='URL', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Автомобильный бренд'
        verbose_name_plural = 'Автомобильные бренды'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('view_brand', kwargs={'slug_brand': self.slug})


class Comments(models.Model):
    content = models.TextField(verbose_name='Комментарии', blank=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    car = models.ForeignKey('Cars', on_delete=models.PROTECT, verbose_name='Автомобиль',)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь',)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        # order_with_respect_to = 'car'  # упорядочивание комментариев к постам об авто
        ordering = ['-create_at']


class AvgUser(models.Model):  # Модель, хранящая дополнительные данные о зарегистрированном пользователе
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


# Привязываем к сигналу добавления комментария, функцию отправки сообщения
post_save.connect(send_message_from_comment, sender=Comments)
