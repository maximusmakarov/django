from django.shortcuts import render
import datetime




'''для главной страницы'''


def index(request):
    context = {
        'page_title': 'главная'
    }
    return render(request, "mainapp/index.html", context)


'''для страницы c контактами'''


def contact(request):
    locations =[
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


'''для страницы c продуктами'''


def products(request):
    context = {
        'page_title': 'каталог'
    }
    return render(request, 'mainapp/products.html', context)


