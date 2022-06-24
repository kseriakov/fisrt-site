from django.contrib import admin
from django.utils.safestring import mark_safe

from cars.models import *


class CarsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'year', 'eng_capacity', 'engine_power', 'type_of_engine', 'transmission',
                    'drive', 'get_image', 'is_published', 'create_at',)

    list_display_links = ('__str__', 'get_image',)

    fields = ('brand', 'title', 'slug', 'year', 'engine_capacity', 'engine_power', 'type_of_engine', 'transmission',
                    'drive', 'get_image', 'image', 'content', 'is_published', 'create_at', )

    readonly_fields = ('create_at', 'get_image')


    def get_image(self, obj):
        if obj.image:
            # mark_safe - помечает строку как html код и не экранирует ее
            return mark_safe(f'<img src="{obj.image.url}" width=75px>')
        else:
            return 'Фото не установлено'

    @admin.display(description='Объем двигателя')
    def eng_capacity(self, obj):
        return mark_safe(f'{obj.engine_capacity} м<sup>3</sup>')


class BrandsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class CommentsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Cars, CarsAdmin)
admin.site.register(Brands, BrandsAdmin)
admin.site.register(Comments, CommentsAdmin)


admin.site.site_header = 'Админ-панель сайта об авто'
