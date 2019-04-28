from django.db import models
from django.conf import settings
from mainapp.models import Product
from functools import reduce
from operator import mul


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)


    @property
    def product_cost(self):
        # "return cost of all products this type"
        return self.product.price * self.quantity

    # @property
    # def total_number(self):
    #     # "return total quantity for user"
    #     return sum(map(lambda x: x.quantity, self.user.basket.select_related('user')))
    #
    # @property
    # def total_amount(self):
    #     # "return total cost for user"
    #     return sum(map(lambda x: x.product_cost, self.user.basket.select_related()))

    @property
    def total_number(self):
        "return total quantity for user"
        quantity = Basket.objects.filter(user=self.user)
        quantity = quantity.aggregate(models.Sum('quantity')).get('quantity__sum', 0)
        return quantity

    @property
    def total_amount(self):
        "return total cost for user"
        _items = Basket.objects.filter(user=self.user)
        _items = _items.values_list('product__price', 'quantity')
        return reduce(lambda x, b: x + mul(*b), _items, 0)
