import uuid
import base64
import pytz

from django.shortcuts import redirect, render
from django.views import generic
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core.files.base import ContentFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.utils import timezone
from django_pandas.io import read_frame

import pandas as pd

from apps.utils.utils import SideBarSelectedMixin
from apps.product.models import Product, ProductTagImage, ProductBarcode
from apps.product.forms import ProductForm, UploadFileForm
from apps.product.utils import extract_data_from_tag
from apps.product.tasks import process_image_data

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openpyxl import load_workbook

from apps.utils.utils import SideBarSelectedMixin
from apps.product.models import (
    Product,
    ProductTagImage,
    ProductBarcode,
    PTFileEntry,
    PTStatus,
)
from apps.department.models import Department, Category, SubCategory, Brand
from apps.product.serializers import (
    PTFileEntrySerializer,
    PTFileEntryCreateSerializer,
    DepartmentSerializer,
    CategorySerializer,
    SubCategorySerializer,
    BrandSerializer,
)
from apps.product.forms import ProductForm
from apps.product.utils import extract_data_from_tag
from apps.product.tasks import process_image_data
from apps.product.models import ProcessingStatus


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        upload_form = UploadFileForm()
        context["upload_form"] = upload_form
        batch_list = ProductBarcode.objects.values("batch_id").distinct()
        context["batch_list"] = batch_list
        return context


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
                print("tag_image", tag_image)
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


class UploadFileView(FormView):
    template_name = "pages/product/barcode_list.html"
    form_class = UploadFileForm
    success_url = "product:barcode_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = "Success"
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES["file"]

            workbook = load_workbook(uploaded_file, read_only=True)
            sheet = workbook.active

            processing_entries = PTFileEntry.objects.filter(status=PTStatus.PENDING)
            barcode_product_number = (
                ProductBarcode.objects.all()
                .values("batch_id")
                .distinct("batch_id")
                .count()
            )
            print("barcode_product_number", barcode_product_number)
            tz = pytz.timezone("Asia/Kolkata")
            current_time = timezone.now().astimezone(tz)
            formatted_time = current_time.strftime("%d-%m-%Y:%H-%M-%S")
            custom_id = f"Batch-{ barcode_product_number+1 }-{ formatted_time }"
            for entry in processing_entries:
                count = entry.quantity
                print("quantity", entry.product.id, "++", count)
                matched_products = []

                for index, row in enumerate(sheet.iter_rows()):
                    if index == 0:
                        continue

                    if all(cell.value in (None, "") for cell in row):
                        continue

                    attributes = [cell.value for cell in row]
                    print("rows", attributes)
                    if entry.product.id == attributes[0]:
                        count = count - 1
                        matched_products.append(
                            {
                                "product": entry.product,
                                "barcode": attributes[10],
                                "sold": False,
                            }
                        )

                    print("count",entry.product.id,"**", count)
                    # print(
                    #     "appending object",
                    #     {
                    #         "product": entry.product,
                    #         "barcode": attributes[11],
                    #         "sold": False,
                    #     },s
                    # )
                    # print("matched_productsarray", matched_products)
                    if count == 0:
                        print("enter in count0")
                        for match_item in matched_products:
                            new_product = ProductBarcode.objects.create(
                                batch_id=custom_id,
                                product=match_item["product"],
                                barcode=match_item["barcode"],
                                sold=match_item["sold"],
                            )
                            # print("new_product", new_product)
                            # print("new_record", new_product.product.processed)
                            new_product.save()
                            entry.status = PTStatus.COMPLETED
                            entry.save()
                        break

            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class PTFileEntryView(SideBarSelectedMixin, LoginRequiredMixin, generic.TemplateView):
    model = PTFileEntry
    template_name = "pages/product/pt_entry.html"
    parent = "product"
    segment = "ptfile_entry"


class PTFileEntryListView(
    SideBarSelectedMixin, LoginRequiredMixin, generic.TemplateView
):
    model = PTFileEntry
    template_name = "pages/product/pt_list.html"
    parent = "product"
    segment = "ptfile_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["user_type"] = self.request.user.user_type
        else:
            context["user_type"] = None
        return context


class PTFileEntryAPIView(generics.ListAPIView):
    queryset = PTFileEntry.objects.filter(status="PROCESSING")
    serializer_class = PTFileEntrySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        departments = DepartmentSerializer(Department.objects.all(), many=True).data
        categories = CategorySerializer(Category.objects.all(), many=True).data
        subcategories = SubCategorySerializer(SubCategory.objects.all(), many=True).data
        brands = BrandSerializer(Brand.objects.all(), many=True).data
        data = serializer.data
        result = {
            "data": data,
            "departments": departments,
            "categories": categories,
            "subcategories": subcategories,
            "brands": brands,
        }
        return Response(result)


class PTFileEntryListAPIView(generics.ListAPIView):
    queryset = PTFileEntry.objects.filter(status="PENDING")
    serializer_class = PTFileEntrySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        departments = DepartmentSerializer(Department.objects.all(), many=True).data
        categories = CategorySerializer(Category.objects.all(), many=True).data
        subcategories = SubCategorySerializer(SubCategory.objects.all(), many=True).data
        brands = BrandSerializer(Brand.objects.all(), many=True).data
        data = serializer.data
        result = {
            "data": data,
            "departments": departments,
            "categories": categories,
            "subcategories": subcategories,
            "brands": brands,
        }
        return Response(result)


class PTFileEntryUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            data_list = data.get("data")
            existing_entries = PTFileEntry.objects.filter(status=data.get("status"))
            existing_ids = [entry.id for entry in existing_entries]
            incoming_ids = [int(entry[0]) if entry[0] else None for entry in data_list]

            ids_to_delete = list(set(existing_ids) - set(incoming_ids))
            PTFileEntry.objects.filter(id__in=ids_to_delete).delete()
            # Update PTFileEntry and Product
            from apps.department.models import SubCategory

            for data in data_list:
                entry_id = data[0]  # PTFileEntry ID
                product_data = {
                    # 'id': data[1],
                    "article_number": data[2],
                    "department_id": data[3],
                    "category_id": data[4],
                    "subcategory": SubCategory.objects.get(id=data[5]),
                    "brand_id": data[6],
                }
                ptfile_entry_data = {
                    "size": data[7],
                    "quantity": data[8],
                    "color": data[9],
                    "mrp": data[10],
                    "wsp": data[11],
                }

                print(entry_id)

                if entry_id:
                    # Update existing PTFileEntry and its associated Product
                    pt_file_entry = PTFileEntry.objects.get(id=entry_id)
                    product = pt_file_entry.product
                    for key, value in product_data.items():
                        setattr(product, key, value)
                    product.save()
                    print("Product updated")
                    print("updating pt file")
                    serializer = PTFileEntrySerializer(
                        pt_file_entry, data=ptfile_entry_data, partial=True
                    )
                else:
                    product = Product.objects.create(**product_data)
                    instance = PTFileEntry.objects.last()
                    serializer = PTFileEntryCreateSerializer(instance, data=ptfile_entry_data, partial=True)
                    print("done")
                if serializer.is_valid():
                    serializer.save(status=PTStatus.PENDING)
                else:
                    print(serializer.errors)
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(
                {"message": "Data updated successfully", "success": True},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            # Handle other exceptions
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CategoryByDepartmentView(View):

    def post(self, request, *args, **kwargs):
        # Retrieve department_id from the request
        department_name = request.POST.get("department_name")
        print("department_name", department_name)
        try:
            department = Department.objects.get(department_name=department_name)

            categories = Category.objects.filter(department=department)

            categories_list = [category.name for category in categories]

            return JsonResponse({"categories": categories_list})

        except Department.DoesNotExist:
            return JsonResponse(
                {"error": f"Department with name {department_name} does not exist"},
                status=404,
            )


class SubCategoryByCategoryView(View):

    def post(self, request, *args, **kwargs):
        # Retrieve department_id from the request
        category_name = request.GET.get("category_name")
        try:
            category = Category.objects.get(category_name=category_name)

            subCategories = SubCategory.objects.filter(category=category)

            sub_categories_list = [subCategory.name for subCategory in subCategories]

            return JsonResponse({"categories": sub_categories_list})

        except Category.DoesNotExist:
            return JsonResponse(
                {"error": f"Department with name {category_name} does not exist"},
                status=404,
            )


class BarcodeBatchDetailsView(SideBarSelectedMixin, LoginRequiredMixin, View):
    template_name = "pages/product/barcode_batch_detail.html"

    def get(self, request, batch_id, *args, **kwargs):
        context = {}
        batch_details = ProductBarcode.objects.filter(batch_id=batch_id)
        context["batch_details"] = batch_details
        return render(request, self.template_name, context)


class ExportPTFilesView(View):
    login_url = "users:account_login"

    def get(self, request, *args, **kwargs):
        queryset = PTFileEntry.objects.filter(status=PTStatus.PENDING).select_related(
            "product", "product__department"
        )

        fields_to_export = [
            "id",
            "product__department__department_name",
            "product__category__category_name",
            "product__subcategory__subcategory_name",
            "product__article_number",
            "color",
            "size",
            "product__brand__brand_name",
            "wsp",
            "mrp",
            "quantity",
        ]
        df = read_frame(queryset, fieldnames=fields_to_export)
        column_mapping = {
            "id": "ItemId",
            "product__department__department_name": "Department",
            "product__category__category_name": "Category",
            "product__subcategory__subcategory_name": "Subcategory",
            "product__article_number": "Article Number",
            "color": "Color",
            "size": "Size",
            "product__brand__brand_name": "Brand",
            "wsp": "WSP",
            "mrp": "MRP",
            "quantity": "Quantity",
        }
        df = df.rename(columns=column_mapping)
        excel_file_path = "data/ptfiles_export.xlsx"
        df.to_excel(excel_file_path, index=False)

        with open(excel_file_path, "rb") as excel_file:
            response = HttpResponse(
                excel_file.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = (
                f'attachment; filename="pending_ptfiles_{pd.Timestamp.now().strftime("%Y-%m-%d")}.xlsx"'
            )

        return response
