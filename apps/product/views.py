from django.shortcuts import render
from django.views import generic

from apps.product.models import Product


class ProductListView(generic.ListView):
    model = Product
    template_name = 'pages/product/product_list.html'
    # login_url = "users:account_login"
    context_object_name = "products"



    
    
    
