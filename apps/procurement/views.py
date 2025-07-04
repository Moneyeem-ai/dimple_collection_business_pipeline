import json

from django.views import generic
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from apps.product.serializers import BrandSerializer
from apps.utils.utils import SideBarSelectedMixin
from apps.product.models import Product
from apps.department.models import Department, Brand
from apps.procurement.models import ProcurementOrder, ProcurementItem
from apps.procurement.forms import ProcurementOrderForm
from apps.procurement.models import AdminApproveStatus
from apps.user.models import UserType
from rest_framework import generics as drf_generics
from rest_framework.response import Response
from rest_framework import status
from apps.department.models import Brand
from apps.procurement.models import AdminApproveStatus


class ProcurementOrderCreateView(
    SideBarSelectedMixin, LoginRequiredMixin, generic.CreateView
):
    model = ProcurementOrder
    form_class = ProcurementOrderForm
    parent = "procurement"
    segment = "create_procurement_order"
    template_name = "pages/procurement_order/create_procurement_order.html"
    success_url = reverse_lazy("procurment_order_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vendors"] = Brand.objects.all()
        context["segment"] = self.segment
        return context

    def post(self, request):
        try:
            data = json.loads(request.body)
            due_date = data.get("due_date")
            vendor_id = data.get("vendor")
            intent_number = data.get("intent_no")
            terms_of_shipment = data.get("tos")
            type = data.get("type")
            brand = Brand.objects.get(id=vendor_id)
            po = f"DC/{brand.brand_code}/{intent_number}"
            if ProcurementOrder.objects.filter(po=po).exists():
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "A procurement order with this PO number already exists.",
                    }
                )
            items = data.get("items")
            order = ProcurementOrder.objects.create(
                due_date=due_date,
                brand=brand,
                intent_number=intent_number,
                terms_of_shipment=terms_of_shipment,
                po=po,
                type = type,
            )
            for item in items:
                article_number = item.get("article_number")
                department_id = item.get("item")
                is_color_code = item.get("is_color_code")
                remarks = item.get("remarks")
                note = item.get("note")
                if is_color_code:
                    color_code = item.get("color")
                    color = None
                else:
                    color = item.get("color")
                    color_code = None

                department = Department.objects.get(id=department_id)
                po_metadata = {"article_number": article_number}
                product, _ = Product.objects.get_or_create(
                    department=department, po_metadata=po_metadata
                )
                ProcurementItem.objects.create(
                    order=order,
                    color=color,
                    color_code=color_code,
                    product=product,
                    quantity_and_size=item.get("quantity_and_size"),
                    remarks=remarks,
                    notes=note
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
        

class ProcurementOrderBottomCreateView(ProcurementOrderCreateView):
    segment = "create_procurement_bottom"
    template_name = "pages/procurement_order/create_po_bottom.html"


class ProcurementOrderKidsCreateView(ProcurementOrderCreateView):
    segment = "create_procurement_kids"
    template_name = "pages/procurement_order/create_po_kids.html"

class ProcurementOrderListView(
    SideBarSelectedMixin, LoginRequiredMixin, generic.ListView
):
    model = ProcurementOrder
    parent = "procurement"
    segment = "procurement_order_list"
    template_name = "pages/procurement_order/procurement_order_list.html"
    context_object_name = "orders"
    ordering = "-created_at"
    paginate_by = 6

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.user_type == UserType.COMPANY_OWNER:
            return ProcurementOrder.objects.filter(
                admin_approve_status__in=[
                    AdminApproveStatus.PENDING,
                    AdminApproveStatus.ACCEPTED,
                ]
            ).order_by("-created_at")
        else:
            return ProcurementOrder.objects.filter(
                admin_approve_status=AdminApproveStatus.ACCEPTED
            ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_admin"] = (
            self.request.user.is_superuser
            or self.request.user.user_type == UserType.COMPANY_OWNER
        )
        return context


class ProcurementOrderActionView(LoginRequiredMixin, View):
    def get(self, request, order_id, action, *args, **kwargs):
        order = get_object_or_404(ProcurementOrder, id=order_id)

        if action == "approve":
            order.admin_approve_status = AdminApproveStatus.ACCEPTED
            messages.success(request, "Order approved successfully.")
        elif action == "reject":
            order.admin_approve_status = AdminApproveStatus.REJECTED
            messages.success(request, "Order rejected successfully.")
        else:
            messages.error(request, "Invalid action.")

        order.save()
        return redirect("procurement:procurement_order_list")


class ProcurementOrderRetrieveUpdateView(
    SideBarSelectedMixin, LoginRequiredMixin, generic.TemplateView
):
    model = ProcurementOrder
    parent = "procurement"
    segment = "procurement_order_list"
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

class ProcurementOrderBottomRetrieveUpdateView(ProcurementOrderRetrieveUpdateView):
    segment = "procurement_order_list"
    template_name = "pages/procurement_order/retrieve_update_po_bottom.html"


class ProcurementOrderKidsRetrieveUpdateView(ProcurementOrderRetrieveUpdateView):
    segment = "procurement_order_list"
    template_name = "pages/procurement_order/retrieve_update_po_kids.html"
# class ProcurementOrderUpdateView(LoginRequiredMixin, UpdateView):
#     model = ProcurementOrder
#     form_class = ProcurementOrderForm
#     template_name = "pages/procurement_order/update_procurement_order.html"
#     context_object_name = "order"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["vendors"] = Brand.objects.all()
#         context["order"] = self.object
#         context["items"] = self.object.procurement_order.all()
#         return context

#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def form_valid(self, form):
#         self.object = form.save()
#         data = json.loads(self.request.body)
#         items = data.get('items')

#         # Update ProcurementOrder fields
#         self.object.due_date = data.get('due_date')
#         self.object.intent_number = data.get('intent_no')
#         self.object.terms_of_shipment = data.get('tos')
#         self.object.brand = get_object_or_404(Brand, id=data.get('vendor'))
#         self.object.save()

#         for item in items:
#             item_id = item.get("item_id")
#             if item_id:
#                 # Update existing item
#                 po_item = get_object_or_404(ProcurementItem, id=item_id)
#                 po_item.remarks = item.get("remarks", po_item.remarks)
#                 po_item.notes = item.get("notes", po_item.notes)
#                 po_item.color_code = item.get("color_code", po_item.color_code)
#                 po_item.color = item.get("color", po_item.color)
#                 po_item.quantity_and_size = item.get("quantity_and_size", po_item.quantity_and_size)
#                 po_item.save()
#             else:
#                 # Create new item
#                 ProcurementItem.objects.create(
#                     order=self.object,
#                     remarks=item.get("remarks"),
#                     notes=item.get("notes"),
#                     color_code=item.get("color_code"),
#                     color=item.get("color"),
#                     product_id=item.get("product_id"),
#                     quantity_and_size=item.get("quantity_and_size")
#                 )
#         return JsonResponse({'status': 'success', 'message': 'Procurement order updated successfully.'})

#     def get_success_url(self):
#         return reverse("procurement:procurement_order_list")