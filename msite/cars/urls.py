from django.urls import path, include
from rest_framework import routers

from cars.views import *


# Простой роутер, реализует обработку запросов
# по следующим адресам: /api/v1/my-cars/; /api/v1/my-cars/<int:pk>
# Имена построенных маршрутов будут выглядеть: basename-list, basename-detail
# router = routers.SimpleRouter()
# router.register(r'my-cars', CarsModelViewSet, basename='cars')

# Дефолт роутер, делает то же самое, что и простой, но по адресу /api/v1/ - выдает доступные API - запросы
router = routers.DefaultRouter()
router.register(r'my-cars', CarsModelViewSet, basename='cars')


urlpatterns = [
    path('', home, name='home'),
    path('add-car/', CreateCar.as_view(), name='add_car'),
    path('edit/<slug:slug_car>', edit_car, name='edit_car'),
    path('car/<slug:slug_car>/', view_car, name='view_car'),
    path('brand/<slug:slug_brand>/', view_brand, name='view_brand'),
    path('photo/<int:photo_id>/', load_photo, name='load_photo'),
    path('edit/brands/', brands_formset, name='brands_formset'),


    # path('api/v1/cars/', api_cars, name='api_cars'),
    # path('api/v1/car/<int:pk>/', api_cars_detail),
    # path('api/v1/brands/', api_brands, name='api_brands'),

    # Реализуем ViewSet - первая строка - вывод всех записей, вторая - вывод одной записи или удаление записи
    path('api/v1/cars/', CarsModelViewSet.as_view({'get': 'list'})),
    path('api/v1/cars/<int:pk>', CarsModelViewSet.as_view({'get': 'list', 'delete': 'destroy'})),
    # Далее упростим обработку HTTP запросов с помощью Роутеров
    path('api/v1/', include(router.urls)),




    path('api/v1/brands/', BrandsAPIView.as_view()),
    path('api/v1/brands/<int:pk>/', BrandsAPIView.as_view()),

    path('api/v1/brands_new/', BrandsAPIListCreate.as_view()),
    path('api/v1/brands_new/<int:pk>/', BrandsAPIRetrieveUpdateDestroy.as_view()),


]
