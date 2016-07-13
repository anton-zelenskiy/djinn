from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = 'Категория'

    def __str__(self):
        return self.category


class Subcategory(models.Model):
    subcategory = models.CharField(max_length=100)
    category = models.ForeignKey(Category)

    class Meta:
        verbose_name_plural = "Подкатегории"
        verbose_name = "Подкатегория"

    def __str__(self):
        return self.subcategory
