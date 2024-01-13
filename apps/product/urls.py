from django.urls import path

from .views import ProductListView, ProductEntryView, ProductBarcodeListView, ProductTagImageView, PTFileEntryListView, PTFileEntryListAPIView, PTFileEntryListView, PTFileEntryUpdateAPIView, ZorderEntryListAPIView, PTFileEntryView

app_name = 'product'

urlpatterns = [
    path('list/', ProductListView.as_view(), name="product_list"),
    path('entry/', ProductEntryView.as_view(), name="product_entry"),
    path('barcode/list/', ProductBarcodeListView.as_view(), name="barcode_list"),
    path('upload_product_image/', ProductTagImageView.as_view(), name='upload_product_image'),
    path('upload_tag_image/<int:id>/', ProductTagImageView.as_view(), name="upload_tag_image"),
    path('ptfile_entry/', PTFileEntryView.as_view(), name='ptfile_entry'),
    path('ptfile_list/', PTFileEntryListView.as_view(), name='ptfile_list'),
    path('api/excel_pt/', PTFileEntryListAPIView.as_view(), name='excel_pt'),
    path('api/excel_update/', PTFileEntryUpdateAPIView.as_view(), name='excel_update'),
    path('api/excel_zorder/', ZorderEntryListAPIView.as_view(), name='excel_zorder'),
]
