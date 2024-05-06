from django.contrib import admin

from .models import Product, ProductImage, PTFileEntry, ProductBarcode, PTFileBatch

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'department', 'category', 'subcategory', 'brand', 'article_number', 'product_images', 'metadata', 'created_at', 'updated_at', 'hash_value']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_image', 'tag_image']

@admin.register(PTFileEntry)
class PTFileEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'status', 'size', 'quantity', 'color', 'per_price', 'mrp', 'invoice_number', 'invoice_date', 'suffix']

@admin.register(ProductBarcode)
class ProductBarcodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'pt_entry', 'barcode', 'sold']

@admin.register(PTFileBatch)
class PTFileBatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'batch_id', 'ptfile_entry_ids', 'is_file_uploaded', 'is_exported', 'is_image_exported']
