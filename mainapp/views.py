import datetime
from mainapp.models import ProductCategory, Product
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from basketapp.models import Basket
import random

'''для главной страницы'''


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    return random.choice(Product.objects.all())


def get_same_products(hot_product):
    return hot_product.category.product_set.exclude(pk=hot_product.pk)


def index(request):
    title = 'главная'
    products_all = Product.objects.all()[:4]
    context = {
        'page_title': title,
        'products': products_all,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', context)


'''для страницы c контактами'''


def contact(request):
    locations = [
        {
            'city': 'Москва',
            'phone': '+7-888-888-8888',
            'email': 'info@geekshop.ru',
            'address': 'В пределах МКАД',
            'time': datetime.datetime.now(),
        },
        {
            'city': 'Санкт-Петербург',
            'phone': '+7-777-888-8888',
            'email': 'spb@geekshop.ru',
            'address': 'В пределах КАД',
            'time': datetime.datetime.now(),
        },
        {
            'city': 'Екатеринбург',
            'phone': '+7-555-888-8888',
            'email': 'ekb@geekshop.ru',
            'address': 'В пределах города',
            'time': datetime.datetime.now(),
        },
    ]
    context = {
        'page_title': 'контакты',
        'locations': locations,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', context)


'''для страницы c продуктами'''


def products(request):
    links_menu = ProductCategory.objects.all()
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    basket = get_basket(request.user)

    context = {
        'page_title': 'каталог',
        'hot_product': hot_product,
        'same_products': same_products,
        'links_menu': links_menu,
        'basket': basket,
    }
    return render(request, 'mainapp/products.html', context)


def category(request, pk):
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if int(pk) == 0:
            products_by_category = {'name': 'все'}
            products_all = Product.objects.all().order_by('price')
        else:
            products_by_category = get_object_or_404(ProductCategory, pk=pk)
            products_all = products_by_category.product_set.order_by('price')

        context = {
            'title': 'продукты',
            'links_menu': links_menu,
            'category': products_by_category,
            'products': products_all,
            'basket': get_basket(request.user)
        }

        return render(request, 'mainapp/products_list.html', context)
