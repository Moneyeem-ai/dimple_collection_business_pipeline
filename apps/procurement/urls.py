from django.urls import path

from .views import ProcurmentOrderCreateView, ProcurmentOrderListView


app_name = 'procurement'


urlpatterns = [
    path('create/', ProcurmentOrderCreateView.as_view(), name='create_procurment_order'),
    path('list/', ProcurmentOrderListView.as_view(), name='procurment_order_list'),
]
