from django.views import generic
from django.urls import reverse_lazy

from apps.utils.utils import SideBarSelectedMixin

from .models import ProcurementOrder
from .forms import ProcurementOrderForm


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
