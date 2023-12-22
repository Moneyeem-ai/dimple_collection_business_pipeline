from django.urls import path

from .views import ProductListView, ProductEntryView, ProductBarcodeListView, ProductImageUploadView, ExtractProductInfoView

app_name = 'product'

urlpatterns = [
    path('list/', ProductListView.as_view(), name="product_list"),
    path('entry/', ProductEntryView.as_view(), name="product_entry"),
    path('barcode/list/', ProductBarcodeListView.as_view(), name="barcode_list"),
    path('extract_info/', ExtractProductInfoView.as_view(), name='extract_info'),
    path('upload_image/<int:id>/', ProductImageUploadView.as_view(), name="upload_image")
]
