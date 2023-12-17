from django.urls import path
from .views import ProductEntryView
app_name = 'product'

urlpatterns = [
    # path('list/', )
    path('entry/', ProductEntryView.as_view(),name="product_entry")
]
