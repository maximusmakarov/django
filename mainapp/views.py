import datetime
import random

from django.shortcuts import render, get_object_or_404

from mainapp.models import ProductCategory, Product


def get_basket(request):
    if request.user.is_authenticated:
        return request.user.basket.all()
    else:
        return []


def get_hot_product():
    return random.choice(Product.objects.filter(is_active=True))


def get_same_products(hot_product):
    return hot_product.category.product_set.filter(is_active=True).exclude(pk=hot_product.pk)


def get_menu():
    return ProductCategory.objects.filter(is_active=True)


def index(request):
    title = 'главная'
    products_all = Product.objects.all()[:4]
    context = {
        'page_title': title,
        'products': products_all,
        'basket': get_basket(request)
    }
    return render(request, 'mainapp/index.html', context)


def category(request, pk):

    if pk is not None:
        if int(pk) == 0:
            products_by_category = {'name': 'все'}
            products_all = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
        else:
            products_by_category = get_object_or_404(ProductCategory, pk=pk)
            products_all = products_by_category.product_set.filter(is_active=True).order_by('price')

        context = {
            'title': 'продукты',
            'links_menu': ProductCategory.objects.all(),
            'category': products_by_category,
            'products': products_all,
            'basket': get_basket(request)
        }

        return render(request, 'mainapp/products_list.html', context)


def products(request):
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    context = {
        'page_title': 'каталог',
        'links_menu': get_menu(),
        'basket': get_basket(request),
        'hot_product': hot_product,
        'same_products': same_products,

    }
    return render(request, 'mainapp/products.html', context)


def product(request, pk):

    context = {
        'title': 'продукт',
        'links_menu': get_menu(),
        'basket': get_basket(request),
        'object': get_object_or_404(Product, pk=pk),
    }

    return render(request, 'mainapp/product.html', context)


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
        'basket': get_basket(request)
    }
    return render(request, 'mainapp/contact.html', context)



