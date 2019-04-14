from django.shortcuts import render
from authapp.models import ShopUser
from mainapp.models import ProductCategory


def index(request):
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': 'админка/пользователи',
        'objects': users_list
    }

    return render(request, 'adminapp/index.html', context)


def categories(request):

    object_list = ProductCategory.objects.all()

    content = {
        'title': 'админка/категории',
        'object_list': object_list
    }

    return render(request, 'adminapp/productcategory_list.html', content)

