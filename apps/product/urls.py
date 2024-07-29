from django.urls import path

from .views import (
    ProductListView,
    ProductEntryView,
    BatchListView,
    ProductBarcodeListView,
    ProductImageView,
    PTFileEntryListView,
    PTFileEntryListAPIView,
    PTFileEntryListView,
    PTFileEntryUpdateAPIView,
    PTFileEntryAPIView,
    PTFileEntryView,
    UploadFileView,
    ExportPTFilesView,
    ExportImagesAPIView,
    MarkPOExportedView,
)

app_name = "product"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("list/", ProductListView.as_view(), name="product_list"),
    path("entry/", ProductEntryView.as_view(), name="product_entry"),
    path("barcode/list/", ProductBarcodeListView.as_view(), name="barcode_list"),
    path("upload_product_image/", ProductImageView.as_view(), name="upload_product_image"),
    path("upload_tag_image/<int:id>/", ProductImageView.as_view(), name="upload_tag_image"),
    path("upload_z_file/<int:batch_id>", UploadFileView.as_view(), name="upload_z_file"),
    path("ptfile_entry/", PTFileEntryView.as_view(), name="ptfile_entry"),
    path("ptfile/batches/", BatchListView.as_view(), name="batch_list"),
    path("ptfile_list/<int:batch_id>/", PTFileEntryListView.as_view(), name="ptfile_list"),
    path('export_images/<int:batch_id>/', ExportImagesAPIView.as_view(), name='export_images'),
    path("api/ptfile_entry/", PTFileEntryAPIView.as_view(), name="api_ptfile_entry"),
    path("api/ptfile_update/", PTFileEntryUpdateAPIView.as_view(), name="api_ptfile_update"),
    path("api/ptfile_list/<int:batch_id>/", PTFileEntryListAPIView.as_view(), name="api_ptfile_list"),
    path("export-batch-to-excel/<int:batch_id>/", ExportPTFilesView.as_view(), name="export_ptfiles"),
    path("export_po/<int:batch_id>/", MarkPOExportedView.as_view(), name="export_for_po"),
]
