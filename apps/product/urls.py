from django.urls import path

from .views import ProductListView, ProductEntryView, ProductBarcodeListView, ProductTagImageView, PTFileEntryListView, UpdateMovieView, CreateMovieView, PTFileEntryListAPIView, PTFileEntryListExcelView, PTFileEntryUpdateAPIView, ZorderEntryListAPIView, ZorderFileEntryListExcelView

app_name = 'product'

urlpatterns = [
    path('list/', ProductListView.as_view(), name="product_list"),
    path('entry/', ProductEntryView.as_view(), name="product_entry"),
    path('barcode/list/', ProductBarcodeListView.as_view(), name="barcode_list"),
    path('upload_product_image/', ProductTagImageView.as_view(), name='upload_product_image'),
    path('upload_tag_image/<int:id>/', ProductTagImageView.as_view(), name="upload_tag_image"),
    path('ptfile_list/', PTFileEntryListView.as_view(), name='ptfile_list'),
    path('create/', CreateMovieView.as_view(), name='create'),
    path('update/', UpdateMovieView.as_view(), name='update'),
    path('ptfile/', PTFileEntryListExcelView.as_view(), name='ptfile'),
    path('api/excel_pt/', PTFileEntryListAPIView.as_view(), name='excel_pt'),
    path('api/excel_update/', PTFileEntryUpdateAPIView.as_view(), name='excel_update'),
    path('api/excel_zorder/', ZorderEntryListAPIView.as_view(), name='excel_zorder'),
    path('zorder/', ZorderFileEntryListExcelView.as_view(), name='zorder'),
]
