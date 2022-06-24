from django import template
from django.core.cache import cache
from django.db.models import Count

from ..models import *

register = template.Library()


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    return instance._meta.get_field(field_name).verbose_name


@register.simple_tag
def get_verbose_field_name_in_form(field_name):
    return Cars._meta.get_field(field_name).verbose_name


@register.inclusion_tag('cars/list_of_brands.html', takes_context=True)
def get_list_of_brands(context):
    # Здесь мы кэшируем список брендов
    brands = cache.get('brands')
    if not brands:
        cache.set('brands', Brands.objects.annotate(cnt=Count('cars')).filter(cnt__gt=0), timeout=30)
        brands = cache.get('brands')
    brand_selected = context.get('brand_selected')
    return {'brands': brands, 'brand_selected': brand_selected}


@register.inclusion_tag('cars/comments.html')
def get_all_comments(car):
    comments = car.comments_set.all()
    return {'comments': comments}


@register.inclusion_tag('cars/comments_bar.html')
def get_5_last_comments():
    comments = Comments.objects.all()[0:5]
    cars_for_comments = Cars.objects.filter(comments__in=comments).order_by('comments').select_related('brand')
    res = []
    for i, comm in enumerate(comments):
        res.append([comm, cars_for_comments[i]])

    return {'set_of_comments': res}
