from django.db import models
from django.conf import settings
from mainapp.models import Product
from functools import reduce
from operator import mul


class BasketQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super().delete(*args, **kwargs)


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)

    @property
    def product_cost(self):
        # "return cost of all products this type"
        return self.product.price * self.quantity

    @property
    def total_number(self):
        """"return total quantity for user"""
        quantity = Basket.objects.filter(user=self.user)
        quantity = quantity.aggregate(models.Sum('quantity')).get('quantity__sum', 0)
        return quantity

    @property
    def total_amount(self):
        """return total cost for user"""
        _items = Basket.objects.filter(user=self.user)
        _items = _items.values_list('product__price', 'quantity')
        return reduce(lambda x, b: x + mul(*b), _items, 0)

    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete()
