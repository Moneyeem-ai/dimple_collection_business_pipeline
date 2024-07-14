from django.urls import path

from .views import (
    ProcurementOrderCreateView,
    ProcurementOrderListView,
    ProcurementOrderRetrieveUpdateView,
    ProcurementOrderActionView
)


app_name = "procurement"


urlpatterns = [
    path(
        "create/", ProcurementOrderCreateView.as_view(), name="create_procurement_order"
    ),
    path("list/", ProcurementOrderListView.as_view(), name="procurement_order_list"),
    path('action/<int:order_id>/<str:action>/', ProcurementOrderActionView.as_view(), name='procurement_order_action'),
    path("<int:pk>/", ProcurementOrderRetrieveUpdateView.as_view(), name="procurement_detail"),
]
