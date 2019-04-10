from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.urls import reverse
from authapp.forms import ShopUserLoginForm
from authapp.forms import ShopUserRegisterForm
from authapp.forms import ShopUserEditForm
# Create your views here.


def login(request):

    form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopUserLoginForm()

    context = {
        'title': 'Вход в систему',
        'form': form
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):

    if request.method == 'POST':
        form = ShopUserRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        form = ShopUserRegisterForm()

    context = {
        'title': 'регистрация',
        'form': form
    }

    return render(request, 'authapp/register.html', context)


def update(request):

    if request.method == 'POST':
        form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:update'))
    else:
        form = ShopUserEditForm(instance=request.user)

    context = {
        'title': 'редактирование',
        'form': form
    }

    return render(request, 'authapp/update.html', context)
