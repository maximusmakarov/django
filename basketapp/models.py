from functools import reduce
from operator import mul

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from mainapp.models import Product

# class BasketQuerySet(models.QuerySet):
#
#     def delete(self, *args, **kwargs):
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#         super().delete(*args, **kwargs)


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @cached_property
    def get_items(self):
        return Basket.objects.select_related()

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    @property
    def product_cost(self):
        """return cost of all products this type"""
        return self.product.price * self.quantity

    @property
    def total_number(self):
        """"return total quantity for user"""
        quantity = self.get_items.aggregate(models.Sum('quantity')).get('quantity__sum', 0)
        return quantity

    @property
    def total_amount(self):
        """return total cost for user"""
        _items = self.get_items.values_list('product__price', 'quantity')
        return reduce(lambda x, b: x + mul(*b), _items, 0)

    # @property
    # def product_cost(self):
    #     return self.product.price * self.quantity
    #
    # @property
    # def total_number(self):
    #     return sum(list(map(lambda x: x.quantity, self.get_items)))
    #
    # @property
    # def total_amount(self):
    #     return sum(list(map(lambda x: x.product_cost, self.get_items)))
