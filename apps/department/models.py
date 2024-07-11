from django.db import models


class Department(models.Model):
    department_name = models.CharField(max_length=64)
    prefix = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.department_name


class Category(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='categories')
    category_name = models.CharField(max_length=64, blank=True)
    hsn_code = models.CharField(max_length=64, blank=True, null=True)
    prefix = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f"{self.category_name}({self.department})"


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    subcategory_name = models.CharField(max_length=64)
    prefix = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.subcategory_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=64)
    brand_code = models.CharField(max_length=64, null=True, blank=True)
    supplier_name = models.CharField(max_length=128, null=True, blank=True)
    suffix = models.CharField(max_length=64, null=True, blank=True)
    address = models.TextField(default=None, null=True, blank=True)

    def __str__(self):
        return self.brand_name
    

class Size(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='sizes')
    size_value = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.size_value


class Color(models.Model):
    color_name = models.CharField(max_length=64)

    def __str__(self):
        return self.color_name