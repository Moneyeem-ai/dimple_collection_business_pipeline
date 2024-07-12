from django.contrib import admin

from .models import ProcurementOrder, ProcurementItem, ProcuredProduct, UnauthorizedProduct

@admin.register(ProcurementOrder)
class ProcurementOrderAdmin(admin.ModelAdmin):
    list_display = ['status', 'brand', 'intent_number', 'terms_of_shipment', 'due_date', 'created_at', 'updated_at']

@admin.register(ProcurementItem)
class ProcurementItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'color', 'product', 'quantity_and_size', 'created_at', 'updated_at']

@admin.register(ProcuredProduct)
class ProcuredProductAdmin(admin.ModelAdmin):
    list_display = ['po_items', 'pt_entries']

@admin.register(UnauthorizedProduct)
class UnauthorizedProductAdmin(admin.ModelAdmin):
    list_display = ['status', 'pt_entry']
