from django.urls import path
from .views import *

app_name = 'product'

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product_list')
]
