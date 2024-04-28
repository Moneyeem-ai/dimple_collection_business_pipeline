from django.contrib import admin
from apps.department.models import Department,Category,SubCategory, Brand, Size
# Register your models here.
admin.site.register(Department)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(Size)