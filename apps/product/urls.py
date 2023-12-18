from django.urls import path

from .views import ProductListView, ProductEntryView, BarcodeListView,ImageUploadView

app_name = 'product'

urlpatterns = [
    path('list/', ProductListView.as_view(), name="product_list"),
    path('entry/', ProductEntryView.as_view(), name="product_entry"),
    path('barcode/list/', BarcodeListView.as_view(), name="barcode_list"),
    path('image_upload/', ImageUploadView.as_view(), name='image_upload'),
]
