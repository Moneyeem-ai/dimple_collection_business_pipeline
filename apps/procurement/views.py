from django.views import generic
from django.urls import reverse_lazy

from .models import ProcurementOrder
from .forms import ProcurementOrderForm


class ProcurementOrderCreateView(generic.CreateView):
    model = ProcurementOrder
    form_class = ProcurementOrderForm
    template_name = 'pages/procurement_order/create_procurement_order.html'
    success_url = reverse_lazy('procurment_order_list')


class ProcurementOrderListView(generic.ListView):
    model = ProcurementOrder
    template_name = 'pages/procurement_order/procurement_order_list.html'
    context_object_name = 'orders'
