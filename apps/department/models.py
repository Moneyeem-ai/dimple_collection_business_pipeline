from django.db import models


class Department(models.Model):
    department_name = models.CharField(max_length=64)
    suffix = models.CharField(max_length=64, null=True, blank=True)
    hsn_code = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.department_name


class Category(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=64, blank=True)
    suffix = models.CharField(max_length=64, null=True)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_name = models.CharField(max_length=64)
    suffix = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.subcategory_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=64)
    brand_code = models.CharField(max_length=64, null=True, blank=True)
    supplier_name = models.CharField(max_length=128, null=True, blank=True)
    prefix = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.brand_name
    

class Size(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    size_value = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.size_value
