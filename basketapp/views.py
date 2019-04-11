from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product
from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required
def index(request):
    basket_items = request.user.basket.order_by('product__category')

    context = {
        'title': 'корзина',
        'basket_items': basket_items,
    }

    return render(request, 'basketapp/index.html', context)


@login_required
def add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('main:product',
                                            kwargs={
                                                'pk': pk,
                                            }))

    product = get_object_or_404(Product, pk=pk)
    basket_add = Basket.objects.filter(user=request.user, product=product).first()

    if not basket_add:
        basket_add = Basket(user=request.user, product=product)

    basket_add.quantity += 1
    basket_add.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, pk):
    get_object_or_404(Basket, pk=pk).delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
