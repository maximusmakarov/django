import datetime
import random

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from mainapp.models import ProductCategory, Product


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        _category = cache.get(key)
        if _category is None:
            _category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, _category)
        return _category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(is_active=True).select_related('category').order_by('price')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.filter(is_active=True).select_related('category').order_by('price')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        _product = cache.get(key)
        if _product is None:
            _product = get_object_or_404(Product, pk=pk)
            cache.set(key, _product)
        return _product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_in_category(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category{pk}'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True). \
                order_by('price')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    return random.choice(get_products())


def get_same_products(hot_product):
    return hot_product.category.product_set.filter(is_active=True).exclude(pk=hot_product.pk)


def get_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def index(request):
    context = {
        'page_title': 'главная',
    }
    return render(request, 'mainapp/index.html', context)


def category(request, pk, page=1):

    if pk is not None:
        if int(pk) == 0:
            _category = {
                'pk': 0,
                'name': 'все',
            }
            _products = get_products()
        else:
            _category = get_category(pk)
            _products = get_products_in_category(pk)

        paginator = Paginator(_products, 2)
        try:
            _products = paginator.page(page)
        except PageNotAnInteger:
            _products = paginator.page(1)
        except EmptyPage:
            _products = paginator.page(paginator.num_pages)

        context = {
            'title': 'продукты',
            'category': _category,
            'products': _products,
            'links_menu': get_menu(),
        }

        return render(request, 'mainapp/products_list.html', context)


def products(request):
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    context = {
        'page_title': 'каталог',
        'hot_product': hot_product,
        'same_products': same_products,
        'links_menu': get_menu()

    }
    return render(request, 'mainapp/products.html', context)


def product(request, pk):

    context = {
        'title': 'продукт',
        'object': get_product(pk),
        'links_menu': get_menu(),
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
    }
    return render(request, 'mainapp/contact.html', context)
