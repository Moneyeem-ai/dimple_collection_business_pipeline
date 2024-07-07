from django.db import models
from django.utils.translation import gettext_lazy as gtl
from django.contrib.postgres.fields import ArrayField

from apps.department.models import Brand
from apps.product.models import Product, PTFileEntry


class ProcurementStatus(models.TextChoices):
    ONGOING = "ongoing", gtl("On Going")
    PAUSE = "pause", gtl("Pause")
    DONE = "done", gtl("Done")


class ProcurementOrder(models.Model):
    status = models.CharField(
        max_length=16,
        choices=ProcurementStatus.choices,
        default=ProcurementStatus.ONGOING,
    )
    brand = models.ForeignKey(Brand, null=True, blank=True, default=None, on_delete=models.CASCADE)
    intent_number = models.CharField(max_length=512, default=None, null=True)
    terms_of_shipment = models.CharField(
        max_length=1024, default="Please Send All Good As soon As Possible.", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProcurementItem(models.Model):
    order = models.ForeignKey(
        ProcurementOrder, related_name="procurement_order", on_delete=models.CASCADE
    )
    color = models.CharField(max_length=512, default=None, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_and_size = models.JSONField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProcuredProduct(models.Model):
    po_items = ArrayField(models.IntegerField(), default=list)
    pt_entries = ArrayField(models.IntegerField(), default=list)


class UnauthorizedProduct(models.Model):
    status = models.CharField(max_length=16)
    pt_entry = models.ForeignKey(PTFileEntry, on_delete=models.CASCADE)
