from django.contrib import admin

from .models import Product, ProductTagImage, PTFileEntry

admin.site.register(Product)
admin.site.register(ProductTagImage)
admin.site.register(PTFileEntry)
