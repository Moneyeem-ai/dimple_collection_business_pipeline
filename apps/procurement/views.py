from django.views import generic
from django.urls import reverse_lazy

from .models import ProcurmentOrder
from .forms import ProcurmentOrderForm


class ProcurmentOrderCreateView(generic.CreateView):
    model = ProcurmentOrder
    form_class = ProcurmentOrderForm
    template_name = 'create_procurment_order.html'
    success_url = reverse_lazy('procurment_order_list')


class ProcurmentOrderListView(generic.ListView):
    model = ProcurmentOrder
    template_name = 'procurment_order_list.html'
    context_object_name = 'orders'
