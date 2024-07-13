import json

from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


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


class ProcurementOrderCreateView(SideBarSelectedMixin, LoginRequiredMixin, generic.CreateView):
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
            due_date = data.get("due_date")
            vendor_id = data.get("vendor")
            brand = Brand.objects.get(id=vendor_id)
            items = data.get("items")
            order = ProcurementOrder.objects.create(
                due_date=due_date,
                brand=brand
            )       
            for item in items:
                article_number = item.get("article_number")
                department_id = item.get("item")

                department = Department.objects.get(
                    id=department_id
                )
                po_metadata = {
                    "article_number": article_number
                }
                product, _ = Product.objects.get_or_create(
                    department=department,
                    po_metadata=po_metadata
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
            print(e)
            return JsonResponse({"status": "error", "message": str(e)})


class ProcurementOrderListView(SideBarSelectedMixin, LoginRequiredMixin, generic.ListView):
    model = ProcurementOrder
    parent = "procurement"
    segment = "procurement_order_list"
    template_name = "pages/procurement_order/procurement_order_list.html"
    context_object_name = "orders"


class ProcurementOrderRetrieveUpdateView(SideBarSelectedMixin, LoginRequiredMixin, generic.TemplateView):
    model = ProcurementOrder
    parent = "procurement"
    segment = "retrieve_update_procurement_order"
    template_name = "pages/procurement_order/retrieve_update_procurement_order.html"
    success_url = reverse_lazy("procurment_order_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = kwargs.get("instance")
        items = instance.procurement_order.all()
        context["items"] = items
        context["po"] = instance
        return context

    def get(self, request, *args, **kwargs):
        instance = ProcurementOrder.objects.get(id=kwargs.get("pk"))
        context = self.get_context_data(instance=instance)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            due_date = data.get("due_date")
            items = data.get("items")
            for item in items:
                item_id = item.get("item_id")
                article_number = item.get("article_number")
                department_id = item.get("item")
                po_item = ProcurementItem.objects.get(id=item_id)
                po_item.quantity_and_size = item.get("quantity_and_size")
                po_item.save()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Procurement order drafted successfully.",
                }
            )
        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": str(e)})
