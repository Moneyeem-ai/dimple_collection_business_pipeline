from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View


from apps.utils.utils import SideBarSelectedMixin

from apps.product.models import Product
from apps.department.models import Department
from .models import ProcurementOrder,ProcurementItem
from .forms import ProcurementOrderForm

import json


class ProcurementOrderCreateView(SideBarSelectedMixin, generic.CreateView):
    model = ProcurementOrder
    form_class = ProcurementOrderForm
    parent = "procurement"
    segment = "create_procurement_order"
    template_name = 'pages/procurement_order/create_procurement_order.html'
    success_url = reverse_lazy('procurment_order_list')


class ProcurementOrderListView(SideBarSelectedMixin, generic.ListView):
    model = ProcurementOrder
    parent = "procurement"
    segment = "procurement_order_list"
    template_name = 'pages/procurement_order/procurement_order_list.html'
    context_object_name = 'orders'

class ProcurementOrderView(View):
    template_name = 'pages/procurement_order/create_procurement_order.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            data = json.loads(request.body)
            items = data.get('items', [])
            order = ProcurementOrder.objects.create(
            )
            for item in items:
                article_number = item.get('article_number')
                department_name = item.get('item')

                department, created = Department.objects.get_or_create(department_name=department_name)

                product = Product.objects.create(
                    article_number=article_number,
                    department=department,
                    category=None,
                    subcategory=None,
                    brand=None,
                    product_images=None,
                    metadata=None,
                    hash_value=None,
                )
                ProcurementItem.objects.create(
                    order=order,
                    color=item.get('color'),
                    product = product,
                    quantity_and_size=item.get('quantity_and_size')
                )
            return JsonResponse({"status": "success", "message": "Procurement order drafted successfully."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})