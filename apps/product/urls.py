from django.urls import path

from .views import ProductListView, ProductEntryView

app_name = 'product'

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product_list'),
    path('entry/', ProductEntryView.as_view(),name="product_entry")
]
