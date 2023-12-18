from django.db import models

from apps.department.models import Department, Category, SubCategory


class Brand(models.Model):
    brand_name = models.CharField(max_length=64)


class Color(models.Model):
    color_name = models.CharField(max_length=32)


class Product(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    article_number = models.CharField(max_length=128, unique=True)
    size = models.IntegerField()
    wsp = models.DecimalField(max_digits=32, decimal_places=2)
    mrp = models.DecimalField(max_digits=32, decimal_places=2)
    image = models.ImageField(upload_to='media/product_images/')

    def __str__(self):
        return self.article_number


class Barcode(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.barcode


class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    # unit = models.CharField(max_length=32)

    def __str__(self):
        return self.quantity


class TagImage(models.Model):
    image = models.ImageField(upload_to='media/product_raw_image/')
    task_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.task_id}'
