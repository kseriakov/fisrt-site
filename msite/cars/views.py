from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib import messages
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from .models import *
from .forms import *
from .cookies import *
from .serializers import *


@login_required  # Для не вошедших на сайт предлагает это сделать, затем если у него нет доступа, выводит 403 страницу
@permission_required(perm='cars.add_brands', raise_exception=True)
def brands_formset(request):
    context = {}
    if request.method == 'POST':
        formset = BrandFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    else:
        formset = BrandFormSet()
    context['formset'] = formset
    context['title'] = 'Изменение брендов авто'

    return render(request, 'cars/brands_formset.html', context)


def load_photo(request, photo_id):
    try:
        route = Cars.objects.get(pk=photo_id).image.path
        return FileResponse(open(route, 'rb'), as_attachment=True)
    except:
        return redirect('home')


@user_passes_test(lambda user: user.is_staff)
def edit_car(request, slug_car):
    car = Cars.objects.get(slug=slug_car)
    if request.method == 'POST':
        form = CarsForm(request.POST, request.FILES, instance=car)
        if not form.fields['image']:
            form.fields['image'] = car.image
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CarsForm(instance=car)
    return render(request, 'cars/edit_car.html', {'form': form, 'title': car, 'car': car})


def home(request):
    cars = Cars.objects.all()
    brands = Brands.objects.all()
    paginator = Paginator(cars, 3)
    if 'page' in request.GET:
        page_num = request.GET['page']
        if int(page_num) > paginator.num_pages:
            raise Http404()
    else:
        page_num = 1
    page = paginator.page(page_num)
    context = {'cars': page.object_list, 'brands': brands, 'page': page, 'paginator': paginator, }
    # Получаем объект HttpResponse()
    response = render(request, 'cars/home.html', context=context)
    # Записываем куки (количество посещений страницы)
    response.set_cookie('cnt', get_visit_in_cookies(request))
    # return HttpResponse(render_to_string('cars/home.html', context=context, request=request))  # Так можно
    return response


def view_brand(request, slug_brand):
    cars = Cars.objects.filter(brand__slug=slug_brand).select_related('brand')
    brand = cars[0].brand
    if not cars:
        raise Http404()
    context = {'cars': cars, 'title': f'Авто бренда {brand}', 'brand_selected': brand, }
    return render(request, 'cars/home.html', context=context)


@login_required
def view_car(request, slug_car):
    car = get_object_or_404(Cars, slug=slug_car)
    if request.method == 'POST':
        form = CommentsForms(request.POST)
        if form.is_valid():
            try:
                form.cleaned_data['car'] = car
                form.cleaned_data['user'] = request.user
                Comments.objects.create(**form.cleaned_data)
                form = CommentsForms()
            except:
                form.add_error('comment', 'Ошибка добавления комментария')

    else:
        form = CommentsForms()

    context = {'car': car, 'form': form, }

    return render(request, 'cars/view_car.html', context=context)


# def set_car(request):
#     if request.method == 'POST':
#         form = CarsForm(request.POST, request.FILES)
#         if form.is_valid():
#             print(form.cleaned_data)
#             form.save()
#             return HttpResponseRedirect(reverse('home'))
#
#     form = CarsForm()
#     return render(request, 'cars/add_car.html', {'form': form})


# class ViewCar(DetailView):
#     model = Cars
#     context_object_name = 'car'
#     slug_url_kwarg = 'slug_car'
#     template_name = 'cars/view_car.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ViewCar, self).get_context_data(**kwargs)
#         context['form'] = self.add_comment(self.request)
#         return context
#
#     def add_comment(self, request):
#         if request.method == 'POST':
#             form = CommentsForms(request.POST)
#             form.fields['cars'] = self.object
#             print("QQQQQ")
#             if form.is_valid():
#
#                 form.save()
#                 return form
#         else:
#             form = CommentsForms()
#
#         return form


class CreateCar(LoginRequiredMixin, CreateView):
    form_class = CarsForm
    template_name = 'cars/add_car.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Страница добавления новости'
        return context

#############################################################################################
# DRF далее!

@api_view(http_method_names=['GET'])  # Декоратор выводит данные в красивой форме RESTa
def api_cars(request):
    if request.method == 'GET':
        cars = Cars.objects.all()
        cars_srl = CarsSerializer(instance=cars, many=True)
        # return JsonResponse(cars_srl.data, safe=False)  # С декоратором нужен свой метод RESTa - Response
        return Response(cars_srl.data)


@api_view(http_method_names=['GET', 'PUT', 'PATCH', 'DELETE'])
def api_cars_detail(request, pk):
    car = get_object_or_404(Cars, pk=pk)
    if request.method == 'GET':
        car_srl = CarsSerializer(instance=car)
        return Response({'car_detail': car_srl.data})

    elif request.method in ['PUT', 'PATCH']:
        car_srl = CarsSerializer(instance=car, data=request.data)
        if car_srl.is_valid():
            car_srl.save()
            return Response({'car_update': car_srl.data})

        return Response(car_srl.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])  # Декоратор выводит данные в красивой форме RESTa
def api_brands(request):
    if request.method == 'GET':
        brands = Brands.objects.all()
        brands_srl = BrandsSerializer(instance=brands, many=True)
        # return JsonResponse(cars_srl.data, safe=False)  # С декоратором нужен свой метод RESTa - Response
        return Response(brands_srl.data)

    elif request.method == 'POST':
        brand_srl = BrandsSerializer(data=request.data)
        if brand_srl.is_valid():
            brand_srl.save()
            return Response({'add_brand': brand_srl.data})

        return Response(brand_srl.errors, status=status.HTTP_400_BAD_REQUEST)


# Далее реализуем контроллер-класс на основе APIView (низкий уровень) для Brands
class BrandsAPIView(APIView):
    def get(self, request):
        brands = Brands.objects.all()
        brands_srl = BrandsSerializer(instance=brands, many=True)
        # return JsonResponse(cars_srl.data, safe=False)  # С декоратором нужен свой метод RESTa - Response
        return Response(brands_srl.data)

    def post(self, request):
        brand_srl = BrandsSerializer(data=request.data)
        if brand_srl.is_valid():
            brand_srl.save()
            return Response({'add_brand': brand_srl.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'error', 'Request is not valid'})

        try:
            brand = Brands.objects.get(pk=pk)
        except:
            return Response({'error': 'Objects is not exists'})

        brand_srl = BrandsSerializer(instance=brand, data=request.data)
        if brand_srl.is_valid():
            brand_srl.save()
            return Response({'update_brand': brand_srl.data})

        return Response(brand_srl.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'error', 'Request is not valid'})

        try:
            brand = Brands.objects.get(pk=pk)
        except:
            return Response({'error': 'Objects is not exists'})

        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Реализуем функционал выше с помощью контроллеров более высокого уровня
# Выдача списка брендов и добавление нового
class BrandsAPIListCreate(generics.ListCreateAPIView):
    queryset = Brands.objects.all()
    serializer_class = BrandsSerializer


# Просмотр, правка, удаление одной записи бренда
class BrandsAPIRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brands.objects.all()
    serializer_class = BrandsSerializer


# Напишем свой класс пагинации
class CarsAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page-size' # параметр в запросе для пользователя, сколько записей выводить - /?page-size=5
    max_page_size = 100


# Реализуем функционал API для работы с Cars с помощью ViewSet
class CarsModelViewSet(ModelViewSet):
    serializer_class = CarsSerializer
    pagination_class = CarsAPIListPagination

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return Cars.objects.filter(pk=pk)
        else:
            return Cars.objects.filter(is_published=True)

# Здесь выводим все бренды авто - доступно по адресу: /api/v1/my-cars/brands/ где brands - название метода
    @action(methods=['GET'], detail=False)
    def brands(self, request):
        brands = Brands.objects.all()
        brands_srl = BrandsSerializer(instance=brands, many=True)
        return Response(data={'brands': brands_srl.data})

# Далее выводим все авто по одному бренду
# url_path - имя в url адрес, этот метод будет доступен по /api/v1/my-cars/<int:pk>/brand/
# url_name - имя в маршруте, полное будет: cars-brand, иначе cars-cars-of-brand
# detail - добавляет параметр <int:pk> - в маршрут
    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated], url_path='brand', url_name='brand')
    def cars_of_brand(self, request, pk=None):
        if not pk:
            return Response(data={'error': 'Do not got number of category'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            in_brand = Brands.objects.get(pk=pk)
        except:
            return Response(data={'error': f'Category having number {pk} not exists'}, status=status.HTTP_404_NOT_FOUND)
        cars = Cars.objects.filter(brand=in_brand)
        if not cars:
            return Response(data={'error': f'Category - {in_brand} do not has cars'}, status=status.HTTP_404_NOT_FOUND)
        cars_srl = CarsSerializer(instance=cars, many=True)
        return Response({f'Brand {in_brand.title}': cars_srl.data})


