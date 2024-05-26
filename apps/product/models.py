from __future__ import absolute_import, unicode_literals
import os
import logging
import hashlib
import pytz

from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

from apps.department.models import Department, Category, SubCategory, Brand, Size, Color

logger = logging.getLogger(__name__)


class ProductImage(models.Model):
    product_image = models.ImageField(
        upload_to="product_images/", null=True, blank=True
    )
    tag_image = models.ImageField(upload_to="tag_images/", null=True, blank=True)


class Product(models.Model):
    department = models.ForeignKey(
        Department, null=True, blank=True, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, max_length=64, null=True, blank=True, on_delete=models.CASCADE
    )
    subcategory = models.ForeignKey(
        SubCategory, max_length=64, null=True, blank=True, on_delete=models.CASCADE
    )
    brand = models.ForeignKey(
        Brand, max_length=64, null=True, blank=True, on_delete=models.CASCADE
    )
    article_number = models.CharField(max_length=128, null=True, blank=True)
    product_images = models.ForeignKey(
        ProductImage, null=True, blank=True, on_delete=models.CASCADE
    )
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    hash_value = models.CharField(max_length=64, null=True, blank=True)


class PTStatus(models.TextChoices):
    ENTRY = "ENTRY"
    LIST = "LIST"
    BARCODE = "BARCODE"
    COMPLETED = "COMPLETED"


# actual PT file data is in this model
class PTFileEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=64, default=PTStatus.ENTRY, choices=PTStatus.choices
    )
    size = models.ForeignKey(
        Size, max_length=64, null=True, blank=True, on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=0)
    color = models.ForeignKey(
        Color, max_length=64, null=True, blank=True, on_delete=models.CASCADE
    )
    color_code = models.CharField(max_length=64, null=True, blank=True)
    pur_price = models.CharField(max_length=128, null=True, blank=True)
    mrp = models.CharField(max_length=128, null=True, blank=True, default=0)
    invoice_number = models.CharField(max_length=128, null=True, blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    suffix = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f"{self.pk}"

    def save(self, *args, **kwargs):
        if not self.pk:
            metadata = getattr(self.product, "metadata", {})
            self.size = Size.objects.filter(id=metadata.get("size_id")).first()
            self.quantity = metadata.get("quantity", 0)
            color_name = metadata.get("color", None)
            self.color = Color.objects.filter(id=metadata.get("color_id")).first()
            self.mrp = metadata.get("mrp", 0)
        return super().save(*args, **kwargs)


class PTFileBatch(models.Model):
    def generate_batch_id():
        tz = pytz.timezone('Asia/Kolkata')
        now = timezone.now().astimezone(tz)
        return now.strftime("%Y-%m-%d_%H:%M:%S")

    batch_id = models.CharField(max_length=20, default=generate_batch_id)
    ptfile_entry_ids = ArrayField(models.IntegerField(), default=list)
    is_file_uploaded = models.BooleanField(default=False)
    is_exported = models.BooleanField(default=False)
    is_image_exported = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.batch_id:
            self.batch_id = self.generate_batch_id()
        super().save(*args, **kwargs)


class ProductBarcode(models.Model):
    pt_entry = models.ForeignKey(
        PTFileEntry, null=True, blank=False, on_delete=models.CASCADE
    )
    barcode = models.CharField(max_length=128, unique=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return str(self.barcode)
