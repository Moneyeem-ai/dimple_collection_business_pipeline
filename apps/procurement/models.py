from django.db import models
from django.utils.translation import gettext_lazy as gtl
from django.contrib.postgres.fields import ArrayField

from apps.department.models import Brand
from apps.product.models import Product, PTFileEntry


class ProcurmentStatus(models.TextChoices):
    ONGOING = "ongoing", gtl("On Going")
    PAUSE = "pause", gtl("Pause")
    DONE = "done", gtl("Done")


class ProcurmentOrder(models.Model):
    status = models.CharField(
        max_length=16,
        choices=ProcurmentStatus.choices,
        default=ProcurmentStatus.ONGOING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProcurmentItem(models.Model):
    order = models.ForeignKey(
        ProcurmentOrder, related_name="procurment_order", on_delete=models.CASCADE
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProcuredProduct(models.Model):
    po_items = ArrayField(models.IntegerField(), default=list)
    pt_entries = ArrayField(models.IntegerField(), default=list)


class UnauthorizedProduct(models.Model):
    status = models.CharField(max_length=16)
    pt_entry = models.ForeignKey(PTFileEntry, on_delete=models.CASCADE)
