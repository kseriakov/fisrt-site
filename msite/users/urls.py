from django.urls import path
from users.views import *

urlpatterns = [

    path('logout/', UserLogout.as_view(), name='logout'),
    path('login/', UserLogin.as_view(), name='login'),
    path('login/success/', success_login, name='success_login'),
    path('logout/success/', success_logout, name='success_logout'),

]
