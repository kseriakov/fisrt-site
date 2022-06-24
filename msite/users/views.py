from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import *


class UserLogin(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    next_page = reverse_lazy('success_login')
    extra_context = {'title': 'Страница аутентификации'}
    # redirect_authenticated_user = True


def success_login(request):
    return render(request, 'users/success_login.html', {'title': 'Успешный вход в аккаунт!'})


class UserLogout(LogoutView):
    next_page = reverse_lazy('success_logout')


def success_logout(request):
    return render(request, 'users/success_logout.html', {'title': 'Вы вышли из аккаунта'})




# def user_login(request):
#     if request.method == 'POST':
#         form_user = UserLoginForm(data=request.POST)
#         if form_user.is_valid():  # при наследовании от AuthenticationForm - сразу проверяется существование пользователя
#         # поэтому проверка user is not None не нужна
#             user_clean_data = form_user.cleaned_data
#             user = authenticate(username=user_clean_data['username'], password=user_clean_data['password'])
#             if user.is_active:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 return HttpResponse('Аккаунт заблокирован')
#         else:
#             errors = form_user.errors
#     else:
#         form_user = UserLoginForm()
#
#     context = {
#         'form': form_user,
#         'title': 'Страница аутентификации'
#     }
#     return render(request, 'users/login.html', context=context)
#


