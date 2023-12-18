from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from apps.utils.utils import SideBarSelectedMixin

from apps.product.models import Product, Barcode
from apps.product.forms import ProductForm


class ProductListView(SideBarSelectedMixin, generic.ListView):
    model = Product
    template_name = 'pages/product/product_list.html'
    login_url = "user:login"
    context_object_name = "products"
    parent = "product"
    segment = "product_list"


class ProductEntryView(SideBarSelectedMixin, CreateView):
    model = Product
    template_name = 'pages/product/product_entry.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_list') 
    parent = "product"
    segment = "product_list"


class BarcodeListView(SideBarSelectedMixin, generic.ListView):
    model = Barcode
    template_name = 'pages/product/barcode_list.html'
    login_url = "user:login"
    context_object_name = "barcodes"
    parent = "product"
    segment = "barcode_list"
