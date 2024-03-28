from django.urls import path

from .views import ProductListView, ProductEntryView, ProductBarcodeListView, ProductTagImageView, PTFileEntryListView, PTFileEntryListAPIView, PTFileEntryListView, PTFileEntryUpdateAPIView, PTFileEntryAPIView, PTFileEntryView,UploadFileView,CategoryByDepartmentView,SubCategoryByCategoryView,BarcodeBatchDetailsView, ExportPTFilesView

app_name = 'product'

urlpatterns = [
    path('list/', ProductListView.as_view(), name="product_list"),
    path('entry/', ProductEntryView.as_view(), name="product_entry"),
    path('barcode/list/', ProductBarcodeListView.as_view(), name="barcode_list"),
    path('upload_product_image/', ProductTagImageView.as_view(), name='upload_product_image'),
    path('upload_tag_image/<int:id>/', ProductTagImageView.as_view(), name="upload_tag_image"),
    path('upload_z_file/', UploadFileView.as_view(), name='upload_z_file'),
    path('ptfile_entry/', PTFileEntryView.as_view(), name='ptfile_entry'),
    path('ptfile_list/', PTFileEntryListView.as_view(), name='ptfile_list'),
    path('api/ptfile_entry/', PTFileEntryAPIView.as_view(), name='api_ptfile_entry'),
    path('api/ptfile_update/', PTFileEntryUpdateAPIView.as_view(), name='api_ptfile_update'),
    path('api/ptfile_list/', PTFileEntryListAPIView.as_view(), name='api_ptfile_list'),
    path('api/get_categories/', CategoryByDepartmentView.as_view(), name='api_get_categories'),
    path('api/get_sub_categories/', CategoryByDepartmentView.as_view(), name='api_get_sub_categories'),
    path('batch_details/<str:batch_id>',BarcodeBatchDetailsView.as_view(),name="batch_details"),
    path('export-ptfile/', ExportPTFilesView.as_view(), name='export_ptfiles')
]
