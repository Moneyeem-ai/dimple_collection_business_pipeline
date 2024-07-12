import json

from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View


from apps.product.serializers import BrandSerializer
from apps.utils.utils import SideBarSelectedMixin
from apps.product.models import Product
from apps.department.models import Department, Brand
from apps.procurement.models import ProcurementOrder, ProcurementItem
from apps.procurement.forms import ProcurementOrderForm
from rest_framework import generics as drf_generics
from rest_framework.response import Response
from rest_framework import status
from apps.department.models import Brand


class ProcurementOrderCreateView(SideBarSelectedMixin, generic.CreateView):
    model = ProcurementOrder
    form_class = ProcurementOrderForm
    parent = "procurement"
    segment = "create_procurement_order"
    template_name = "pages/procurement_order/create_procurement_order.html"
    success_url = reverse_lazy("procurment_order_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vendors"] = Brand.objects.all()
        return context

    def post(self, request):
        try:
            data = json.loads(request.body)
            items_data = data.get("items", [])
            due_date = items_data[0]
            print(due_date)
            vendor_id = items_data[1]
            print(vendor_id)
            items = items_data[2:]
            order = ProcurementOrder.objects.create(
                due_date=due_date,
                brand_id=vendor_id
            )
            print(items_data)        
            for item in items:
                print("IIIIIIIIIIIIIIIIIIIIIIIIIIII")
                print(item)
                article_number = item.get("article_number")
                department_name = item.get("item")

                department, created = Department.objects.get_or_create(
                    department_name=department_name
                )
                po_meta = ''
                product = Product.objects.create(
                    # brand=brand,
                    po_metadata=po_meta
                )
                ProcurementItem.objects.create(
                    order=order,
                    color=item.get("color"),
                    product=product,
                    quantity_and_size=item.get("quantity_and_size"),
                )
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Procurement order drafted successfully.",
                }
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


class ProcurementOrderListView(SideBarSelectedMixin, generic.ListView):
    model = ProcurementOrder
    parent = "procurement"
    segment = "procurement_order_list"
    template_name = "pages/procurement_order/procurement_order_list.html"
    context_object_name = "orders"


class BrandListAPIView(drf_generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
