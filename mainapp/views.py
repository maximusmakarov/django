from django.shortcuts import render


# Create your views here.

'''для главной страницы'''


def index(request):
    return render(request, "mainapp/index.html")


'''для страницы c контактами'''


def contact(request):
    return render(request, 'mainapp/contact.html')


'''для страницы c продуктами'''


def products(request):
    return render(request, 'mainapp/products.html')


