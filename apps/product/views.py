from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from apps.product.models import Product
from apps.product.forms import ProductForm


class ProductListView(generic.ListView):
    model = Product
    template_name = 'pages/product/product_list.html'
    # login_url = "users:account_login"
    context_object_name = "products"


class ProductEntryView(CreateView):
    model = Product
    template_name = 'pages/product/product_entry.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_list') 
