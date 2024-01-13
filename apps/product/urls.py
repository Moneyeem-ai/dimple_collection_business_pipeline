from django.urls import path

from .views import ProductListView, ProductEntryView, ProductBarcodeListView, ProductTagImageView,UploadFileView

app_name = 'product'

urlpatterns = [
    path('list/', ProductListView.as_view(), name="product_list"),
    path('entry/', ProductEntryView.as_view(), name="product_entry"),
    path('barcode/list/', ProductBarcodeListView.as_view(), name="barcode_list"),
    path('upload_product_image/', ProductTagImageView.as_view(), name='upload_product_image'),
    path('upload_tag_image/<int:id>/', ProductTagImageView.as_view(), name="upload_tag_image"),
    path('upload_z_file/', UploadFileView.as_view(), name='upload_z_file'),
    
    # path('create/', CreateMovieView.as_view(), name='create'),
    # path('update/', UpdateMovieView.as_view(), name='update')
]
