from django.contrib import admin

from .models import Product, ProductImage, PTFileEntry,ProductBarcode,PTFileBatch

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(PTFileEntry)
admin.site.register(ProductBarcode)
admin.site.register(PTFileBatch)