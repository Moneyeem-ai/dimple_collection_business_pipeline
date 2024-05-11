from django.contrib import admin
from apps.department.models import Department, Category, SubCategory, Brand, Size, Color

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'department_name', 'prefix']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'department', 'category_name', 'hsn_code', 'prefix']

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'subcategory_name', 'prefix']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand_name', 'brand_code', 'supplier_name', 'suffix']

class SizeAdmin(admin.ModelAdmin):
    list_display = ['id', 'department', 'size_value']

class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'color_name']

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
