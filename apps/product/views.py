import uuid
import base64

from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile

from apps.utils.utils import SideBarSelectedMixin
from apps.product.models import Product, Barcode, TagImage
from apps.product.forms import ProductForm


class ProductListView(SideBarSelectedMixin, generic.ListView):
    model = Product
    template_name = 'pages/product/product_list.html'
    # login_url = "users:account_login"
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
    # login_url = "users:account_login"
    context_object_name = "barcodes"
    parent = "product"
    segment = "barcode_list"


class ImageUploadView(View):
    def post(self, request, *args, **kwargs):
        try:
            image_data = request.body.decode('utf-8').split(',')[1]
            decoded_image_data = base64.b64decode(image_data)
            image_name = uuid.uuid4()
            image_file = ContentFile(decoded_image_data, name=f'{image_name}.png')
            TagImage.objects.create(image=image_file, task_id=image_name)
            context = {
                "department": "Half Sleeves",
                "category": "Category",
                "subcategory": "Subcategory",
                "brand": "Addidas",
                "color": "Red",
                "article_number": "FDKMKNANF231",
                "size": 43,
                "wsp": 123.9,
                "mrp": 150.9
            }
            return JsonResponse({'status': 'success',"context":context})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': str(e)})
