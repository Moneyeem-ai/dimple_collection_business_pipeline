from django.contrib import admin

from .models import Product, ProductTagImage, PTFileEntry,ProductBarcode,PTFileBatch

admin.site.register(Product)
admin.site.register(ProductTagImage)
admin.site.register(PTFileEntry)
admin.site.register(ProductBarcode)
admin.site.register(PTFileBatch)