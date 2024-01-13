import uuid
import base64

from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import CheckboxSelectMultiple, CheckboxInput, DateInput
from django.urls import reverse_lazy

from funky_sheets.formsets import HotView
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.utils.utils import SideBarSelectedMixin
from apps.product.models import Product, ProductTagImage, ProductBarcode, PTFileEntry, PTStatus
from apps.product.serializers import PTFileEntrySerializer, PTFileEntryCreateSerializer
from apps.product.forms import ProductForm
from apps.product.utils import extract_data_from_tag
from apps.product.tasks import process_image_data
from .forms import PTFileEntryFormSet



class ProductListView(SideBarSelectedMixin, LoginRequiredMixin, generic.ListView):
    model = Product
    template_name = "pages/product/product_list.html"
    login_url = "user:login"
    context_object_name = "products"
    parent = "product"
    segment = "product_list"


class ProductBarcodeListView(
    SideBarSelectedMixin, LoginRequiredMixin, generic.ListView
):
    model = ProductBarcode
    template_name = "pages/product/barcode_list.html"
    login_url = "user:login"
    context_object_name = "barcodes"
    parent = "product"
    segment = "barcode_list"


class ProductEntryView(SideBarSelectedMixin, LoginRequiredMixin, generic.TemplateView):
    template_name = "pages/product/product_entry_photo.html"
    form_class = ProductForm
    parent = "product"
    segment = "product_list"

    def get_context_data(self):
        data = self.request.GET
        context = super().get_context_data()
        context["photo"] = "Cloth" if data.get("page") == "1" else "Tag"
        if data.get("page") == "3":
            id = data.get("id")
            product = Product.objects.get(id=id)
            context["form"] = self.form_class(instance=product)
            context["product"] = product
        return context

    def get(self, request):
        if request.GET.get("page") == "3":
            context = self.get_context_data()
            self.template_name = "pages/product/product_entry.html"
            return self.render_to_response(context=context)
        return super().get(request=request)

    def post(self, request):
        id = request.GET.get("id")
        instance = Product.objects.get(id=id)
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return redirect("product:product_entry")


class ProductTagImageView(View):
    def post(self, request, *args, **kwargs):
        try:
            image_data = request.body.decode("utf-8").split(",")[1]
            while len(image_data) % 4 != 0:
                image_data += "="
            decoded_image_data = base64.b64decode(image_data)
            image_name = str(uuid.uuid4())
            image_file = ContentFile(decoded_image_data, name=f"{image_name}.png")
            product_instance = ProductTagImage.objects.create(product_image=image_file)
            context = {"product_id": product_instance.id}
            print("product_id", product_instance.id)
            return JsonResponse({"status": "success", "context": context})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": str(e)})

    def patch(self, request, *args, **kwargs):
        print("hello")
        product_id = kwargs.get("id")

        # tag_image = request.FILES.get("tag_image")
        try:
            image_data = request.body.decode("utf-8").split(",")[1]
            while len(image_data) % 4 != 0:
                image_data += "="
            decoded_image_data = base64.b64decode(image_data)
            image_name = str(uuid.uuid4())
            image_file = ContentFile(decoded_image_data, name=f"{image_name}.png")
            try:
                product_image_instance = ProductTagImage.objects.get(id=product_id)
                product_image_instance.tag_image = image_file
                product_image_instance.save()
                tag_image = product_image_instance.tag_image.name.split("/")[1]
                print("tag_image",tag_image)
                process_image_data.delay(tag_image, product_image_instance.id)
                print("product_id_after", "done save product")
                context = {}
            except Exception as e:
                print(e)
                context = {}
            return JsonResponse({"status": "success", "context": context})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": str(e)})


class ProductImageUploadView(View):
    def post(self, request, *args, **kwargs):
        id = kwargs.get("id")
        try:
            image_data = request.body.decode("utf-8").split(",")[1]
            while len(image_data) % 4 != 0:
                image_data += "="
            decoded_image_data = base64.b64decode(image_data)
            image_name = str(uuid.uuid4())
            image_file = ContentFile(decoded_image_data, name=f"{image_name}.png")
            try:
                product = Product.objects.get(id=id)
                product.product_image = image_file
                tag_image = product.tag_image.name.split("/")[1]
                data = extract_data_from_tag(tag_image)
                for key, value in data.items():
                    setattr(product, key, value)
                product.metadata = data
                product.save()
                context = {"product_id": product.id}
            except Exception as e:
                print(e)
                context = {}
            return JsonResponse({"status": "success", "context": context})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": str(e)})


class PTFileEntryView(SideBarSelectedMixin, LoginRequiredMixin, generic.TemplateView):
    model = PTFileEntry 
    template_name = 'pages/product/pt_entry.html'
    parent = "product"
    segment = "ptfile_entry"


class PTFileEntryListView(SideBarSelectedMixin, LoginRequiredMixin, generic.TemplateView):
    model = PTFileEntry 
    template_name = 'pages/product/pt_list.html'
    parent = "product"
    segment = "ptfile_list"


class PTFileEntryAPIView(generics.ListAPIView):
    queryset = PTFileEntry.objects.filter(status='PROCESSING')
    serializer_class = PTFileEntrySerializer


class PTFileEntryListAPIView(generics.ListAPIView):
    queryset = PTFileEntry.objects.filter(status='PENDING')
    serializer_class = PTFileEntrySerializer


class PTFileEntryUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data_list= request.data
            print("!!!!!!!!!!!")
            print(data_list)
            existing_entries = PTFileEntry.objects.filter(status=PTStatus.PROCESSING)

            existing_ids = [entry.id for entry in existing_entries]
            print(existing_ids)

            incoming_ids = [ int(entry[0]) if entry[0] else None for entry in data_list]
            print(incoming_ids)

            ids_to_delete = list(set(existing_ids) - set(incoming_ids))
            print(ids_to_delete)
            PTFileEntry.objects.filter(id__in=ids_to_delete).delete()

            for data in data_list:
                entry_id = data[0]
                print(data)
                print(entry_id)
                if entry_id:
                    try:
                        pt_file_entry = PTFileEntry.objects.get(id=entry_id)
                        serializer = PTFileEntrySerializer(pt_file_entry, data={'size': data[7],'quantity': data[8], 'color': data[9], 'mrp': data[10], 'wsp': data[11]})
                    except PTFileEntry.DoesNotExist:
                        return Response({'error': f'PTFileEntry not found for ID {entry_id}'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    serializer = PTFileEntryCreateSerializer(data={'product': data[1] , 'size': data[7],'quantity': data[8], 'color': data[9], 'mrp': data[10], 'wsp': data[11]}, many=False)

                print(serializer.is_valid())
                if serializer.is_valid():
                    serializer.save(status=PTStatus.PENDING)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Data updated successfully', 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle other exceptions
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)