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
from apps.product.models import Product, ProductBarcode
from apps.product.forms import ProductForm
from apps.product.utils import extract_data_from_tag


class ProductListView(SideBarSelectedMixin, generic.ListView):
    model = Product
    template_name = 'pages/product/product_list.html'
    login_url = "user:login"
    context_object_name = "products"
    parent = "product"
    segment = "product_list"


class ProductEntryView(SideBarSelectedMixin, generic.TemplateView):
    template_name = 'pages/product/product_entry_tag_photo.html'
    form_class = ProductForm
    parent = "product"
    segment = "product_list"


class ProductBarcodeListView(SideBarSelectedMixin, generic.ListView):
    model = ProductBarcode
    template_name = 'pages/product/barcode_list.html'
    login_url = "user:login"
    context_object_name = "barcodes"
    parent = "product"
    segment = "barcode_list"


class ImageUploadView(View):
    def post(self, request, *args, **kwargs):
        try:
            print("data")
            image_data = request.body.decode('utf-8').split(',')[1]
            print(image_data)
            decoded_image_data = base64.b64decode(image_data)
            image_name = str(uuid.uuid4())
            print(image_name)
            image_file = ContentFile(decoded_image_data, name=f'{image_name}.png')
            print("image_file")
            product = Product.objects.create(tag_image=image_file)
            print(product)
            try:
                data = extract_data_from_tag(f'{image_name}.png')
                for key, value in data.items():
                    setattr(product, key, value)
                product.meta_data = data
                product.save()
                context = {
                    "product_id": product.id
                }
            except Exception as e:
                print(e)
                context = {}
            return JsonResponse({'status': 'success',"context": context})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': str(e)})
