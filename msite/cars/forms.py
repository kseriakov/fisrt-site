from captcha.fields import CaptchaField, CaptchaTextInput
from django.core.exceptions import ValidationError
from django.forms import ModelForm, modelformset_factory, BaseModelFormSet
from django import forms
from .models import *


class CarsForm(ModelForm):

    # Полное определение поля
    # title = forms.CharField(initial='Qwerty', widget=forms.widgets.TextInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='Введите текст:', error_messages={'invalid': 'Неправильный текст'},
                           widget=CaptchaTextInput(attrs={'class': 'form-control mt-2'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].empty_label = "Выберите бренд"

    class Meta:
        model = Cars
        fields = ('brand', 'title', 'year', 'engine_capacity', 'engine_power', 'type_of_engine', 'transmission',
                    'drive', 'image', 'content', 'captcha', )

        labels = {'brand': 'Какой-то бренд'}  # Подпись определена в html

        widgets = {  # Виджеты задают атрибуты тегам Django
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'engine_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'engine_power': forms.NumberInput(attrs={'class': 'form-control'}),
            'type_of_engine': forms.Select(attrs={'class': 'form-control'}),
            'transmission': forms.Select(attrs={'class': 'form-control'}),
            'drive': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if len(title) > 10:
    #         raise ValidationError('Длина заголовка превышает 10 символов')
    #     return title


class BaseBrandFormSet(BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        super(BaseBrandFormSet, self).__init__(*args, **kwargs)
        self.queryset = Brands.objects.all()

    def get_deletion_widget(self):
        return forms.CheckboxInput(attrs={'class': 'form-check-input'})

    def clean(self):
        super().clean()
        if any(self.errors):
            return
        titles = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            title = form.cleaned_data.get('title')
            slug = form.cleaned_data.get('slug')
            if title in titles:
                raise ValidationError('Такой бренд уже существует')
            titles.append(title)


BrandFormSet = modelformset_factory(
    Brands,
    fields='__all__',
    can_delete=True,
    formset=BaseBrandFormSet,
    widgets={
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'slug': forms.TextInput(attrs={'class': 'form-control'}),
    },
)


class CommentsForms(forms.Form):
    content = forms.CharField(label='Ваш комментарий', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    car = forms.CharField(widget=forms.HiddenInput(), required=False)
    user = forms.CharField(widget=forms.HiddenInput(), required=False)
