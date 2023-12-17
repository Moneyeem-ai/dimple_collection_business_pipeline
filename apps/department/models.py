from django.db import models


class Department(models.Model):
    department_name = models.CharField(max_length=64)

    def __str__(self):
        return self.department_name


class Category(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_name = models.CharField(max_length=64)

    def __str__(self):
        return self.subcategory_name
