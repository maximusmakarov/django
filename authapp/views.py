from django.http import HttpResponseRedirect
from django.shortcuts import render
from authapp.forms import ShopUserLoginForm
from django.contrib import auth
from django.urls import reverse
# Create your views here.


def login(request):
    title = 'вход'

    form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))

    context ={
        'title': 'Вход в систему',
        'form': form
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def edit(request):
    pass
