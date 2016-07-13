from django.db import models
from category.models import Category, Subcategory
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Employee(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=1024)
    price = models.IntegerField(null=True, default=0)
    category = models.ManyToManyField(Category)
    subcategory = models.ManyToManyField(Subcategory)

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'
