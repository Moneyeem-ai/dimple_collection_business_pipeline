from django.urls import path

from .views import (
    ProcurementOrderCreateView,
    ProcurementOrderListView,
    BrandListAPIView
)


app_name = "procurement"


urlpatterns = [
    path(
        "create/", ProcurementOrderCreateView.as_view(), name="create_procurement_order"
    ),
    path("list/", ProcurementOrderListView.as_view(), name="procurement_order_list"),
    path("brands/", BrandListAPIView.as_view(), name="brand_list"),
]
