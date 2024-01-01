import uuid
import base64

from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.utils.utils import SideBarSelectedMixin
from apps.product.models import Product, ProductBarcode
from apps.product.forms import ProductForm
from apps.product.utils import extract_data_from_tag

from django.forms import CheckboxSelectMultiple, CheckboxInput, DateInput
from django.urls import reverse_lazy

from funky_sheets.formsets import HotView

from .models import Movie


class ProductListView(SideBarSelectedMixin, LoginRequiredMixin, generic.ListView):
    model = Product
    template_name = 'pages/product/product_list.html'
    login_url = "user:login"
    context_object_name = "products"
    parent = "product"
    segment = "product_list"


class ProductBarcodeListView(SideBarSelectedMixin, LoginRequiredMixin, generic.ListView):
    model = ProductBarcode
    template_name = 'pages/product/barcode_list.html'
    login_url = "user:login"
    context_object_name = "barcodes"
    parent = "product"
    segment = "barcode_list"


class ProductEntryView(SideBarSelectedMixin, LoginRequiredMixin, generic.TemplateView):
    template_name = 'pages/product/product_entry_photo.html'
    form_class = ProductForm
    parent = "product"
    segment = "product_list"

    def get_context_data(self):
        data = self.request.GET
        context = super().get_context_data()
        context["photo"] = "Cloth" if data.get("page") == "2" else "Tag"
        if data.get("page") == '3':
            id = data.get("id")
            product = Product.objects.get(id=id)
            context["form"] = self.form_class(instance=product)
            context["product"] = product
        return context

    def get(self, request):
        if request.GET.get("page") == '3':
            context = self.get_context_data()
            self.template_name = 'pages/product/product_entry.html'
            return self.render_to_response(context=context)
        return super().get(request=request)

    def post(self, request):
        id = request.GET.get("id")
        instance = Product.objects.get(id=id)
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return redirect("product:product_entry")


class ExtractProductInfoView(View):
    def post(self, request, *args, **kwargs):
        try:
            image_data = request.body.decode('utf-8').split(',')[1]
            while len(image_data) % 4 != 0:
                image_data += '='
            decoded_image_data = base64.b64decode(image_data)
            image_name = str(uuid.uuid4())
            image_file = ContentFile(decoded_image_data, name=f'{image_name}.png')
            product = Product.objects.create(tag_image=image_file)
            context = {
                "product_id": product.id
            }
            return JsonResponse({'status': 'success',"context": context})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': str(e)})


class ProductImageUploadView(View):
    def post(self, request, *args, **kwargs):
        id = kwargs.get("id") 
        try:
            image_data = request.body.decode('utf-8').split(',')[1]
            decoded_image_data = base64.b64decode(image_data)
            image_name = str(uuid.uuid4())
            image_file = ContentFile(decoded_image_data, name=f'{image_name}.png')
            try:
                product = Product.objects.get(id=id)
                product.product_image = image_file
                tag_image = product.tag_image.name.split('/')[1]
                data = extract_data_from_tag(tag_image)
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

class CreateMovieView(HotView):
    # Define model to be used by the view
    model = Movie
    # Define template
    template_name = 'pages/test/test.html'
    # Define custom characters/strings for checked/unchecked checkboxes
    checkbox_checked = 'yes' # default: true
    checkbox_unchecked = 'no' # default: false
    # Define prefix for the formset which is constructed from Handsontable spreadsheet on submission
    prefix = 'table'
    # Define success URL
    success_url = reverse_lazy('update')
    # Define fields to be included as columns into the Handsontable spreadsheet
    fields = (
        'id',
        'title',
        'director',
        'release_date',
        'parents_guide',
        'imdb_rating',
        'genre',
        'imdb_link',
    )
    # Define extra formset factory kwargs
    factory_kwargs = {
        'widgets': {
            'release_date': DateInput(attrs={'type': 'date'}),
            'genre': CheckboxSelectMultiple(),
            'parents_guide': CheckboxInput(),
        }
    }
    # Define Handsontable settings as defined in Handsontable docs
    hot_settings = {
        'contextMenu': 'true',
        'autoWrapRow': 'true',
        'rowHeaders': 'true',
        'contextMenu': 'true',
        'search': 'true',
        # When value is dictionary don't wrap it in quotes
        'headerTooltips': {
            'rows': 'false',
            'columns': 'true'
        },
        # When value is list don't wrap it in quotes
        'dropdownMenu': [
            'remove_col',
            '---------',
            'make_read_only',
            '---------',
            'alignment'
        ]
    }

class UpdateMovieView(CreateMovieView):
  template_name = 'pages/test/update.html'
  # Define 'update' action
  action = 'update'
  # Define 'update' button
  button_text = 'Update'