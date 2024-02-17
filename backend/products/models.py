from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)
    
    def search(self, query, user=None):
        lookup = models.Q(title__icontains=query) | models.Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs1 = self.filter(user=user).filter(lookup)
            qs = (qs | qs1).distinct()
        return qs

class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs) -> models.QuerySet:
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)


class Product(models.Model):

    user = models.ForeignKey(User, on_delete = models.SET_NULL, default = 1, null = True)

    title = models.CharField(max_length = 120)
    content = models.TextField(blank = True, null = True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)

    public = models.BooleanField(default=True)

    objects = ProductManager()

    def is_public(self):
        return self.public

    @property
    def sale_price(self):
        return "%.2f" %(float(self.price) * 0.8)
    
    def get_discount(self):
        return "22"