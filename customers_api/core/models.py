from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'customer'
        verbose_name_plural = 'customers'

    def __str__(self):
        return self.name


class FavoriteList(models.Model):
    customer = models.ForeignKey(Customer, related_name='favorites', on_delete=models.CASCADE)
    product_id = models.CharField(max_length=200)

    def __str__(self):
        return self.product_id
