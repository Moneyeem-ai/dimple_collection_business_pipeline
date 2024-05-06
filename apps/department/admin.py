from django.contrib import admin
from apps.department.models import Department, Category, SubCategory, Brand, Size

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'department_name', 'suffix']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'department', 'category_name', 'hsn_code', 'suffix']

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'subcategory_name', 'suffix']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand_name', 'brand_code', 'supplier_name', 'prefix']

class SizeAdmin(admin.ModelAdmin):
    list_display = ['id', 'department', 'size_value']

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Size, SizeAdmin)
