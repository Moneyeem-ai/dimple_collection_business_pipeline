from django.urls import path

from .views import (
    ProcurementOrderCreateView,
    ProcurementOrderListView,
    ProcurementOrderRetrieveUpdateView,
    ProcurementOrderActionView,
    ProcurementOrderBottomCreateView,
    ProcurementOrderKidsCreateView,
    ProcurementOrderBottomRetrieveUpdateView,
    ProcurementOrderKidsRetrieveUpdateView
    # ProcurementOrderUpdateView
)


app_name = "procurement"


urlpatterns = [
    path(
        "create/", ProcurementOrderCreateView.as_view(), name="create_procurement_order"
    ),
    path(
        "create_bottom/", ProcurementOrderBottomCreateView.as_view(), name="create_procurement_order_bottom"
    ),
    path(
        "create_kids/", ProcurementOrderKidsCreateView.as_view(), name="create_procurement_order_kids"
    ),
    path("list/", ProcurementOrderListView.as_view(), name="procurement_order_list"),
    path('action/<int:order_id>/<str:action>/', ProcurementOrderActionView.as_view(), name='procurement_order_action'),
    path("details/<int:pk>/", ProcurementOrderRetrieveUpdateView.as_view(), name="procurement_detail"),
    path("details_bottom/<int:pk>/", ProcurementOrderBottomRetrieveUpdateView.as_view(), name="procurement_bottom_detail"),
    path("details_kids/<int:pk>/", ProcurementOrderKidsRetrieveUpdateView.as_view(), name="procurement_kids_detail"),
    # path('update/<int:pk>/', ProcurementOrderUpdateView.as_view(), name='update_procurement_order'),
]
