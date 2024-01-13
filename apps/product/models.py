from __future__ import absolute_import, unicode_literals
import os
import logging
import hashlib

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


logger = logging.getLogger(__name__)


class ProductTagImage(models.Model):
    product_image = models.ImageField(
        upload_to="product_images/", null=True, blank=True
    )
    tag_image = models.ImageField(upload_to="tag_images/", null=True, blank=True)


class ProcessingStatus(models.TextChoices):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class Product(models.Model):
    department = models.CharField(max_length=64, null=True, blank=True)
    category = models.CharField(max_length=64, null=True, blank=True)
    subcategory = models.CharField(max_length=64, null=True, blank=True)
    brand = models.CharField(max_length=64, null=True, blank=True)
    article_number = models.CharField(max_length=128, null=True, blank=True)
    product_images = models.ForeignKey(
        ProductTagImage, null=True, blank=True, on_delete=models.CASCADE
    )
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    processed = models.CharField(max_length=20, default=ProcessingStatus.PENDING, choices=ProcessingStatus.choices)
    hash_value = models.CharField(max_length=64, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        existing_entry = None
        # logger.info(existing_entry)
        if self.brand and self.article_number:
            # Calculate hash using SHA256
            hash_string = f"{self.department}{self.brand}{self.article_number}"
            hash_value = hashlib.sha256(hash_string.encode()).hexdigest()
            self.hash_value = hash_value
            try:
                existing_entry = Product.objects.get(hash_value=hash_value)
            except Exception as e:
                existing_entry = None
                logger.info("!!!!!!!")
                logger.info(f"Error: {e}")
        if existing_entry and not self.pk:
            logger.info(existing_entry)
            pt_file_data = PTFileEntry.objects.create(product=existing_entry)
            return existing_entry
        else:
            product = super().save(*args, **kwargs)
            return product


class PTStatus(models.TextChoices):
    PROCESSING = "PROCESSING"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


# actual PT file data is in this model
class PTFileEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=64, default=PTStatus.PROCESSING, choices=PTStatus.choices
    )
    size = models.CharField(max_length=128, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    color = models.CharField(max_length=64, null=True, blank=True)
    wsp = models.CharField(max_length=128, null=True, blank=True)
    mrp = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.product.article_number

    def save(self, *args, **kwargs):
        logger.info(self.product)
        if self.product and not self.pk:
            logger.info(self.product.metadata)
            if self.product.metadata:
                metadata = self.product.metadata
                self.size = metadata.get('size', 0)
                self.quantity = metadata.get('quantity', 0)
                self.color = metadata.get('color', '')
                self.mrp = metadata.get('mrp', 0)
                logger.info(self)
        return super().save(*args, **kwargs)


class ProductBarcode(models.Model):
    product = models.ForeignKey(PTFileEntry, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=128, unique=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return self.barcode


class Movie(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-generated primary key
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    release_date = models.DateField()
    parents_guide = models.BooleanField()
    imdb_rating = models.DecimalField(max_digits=4, decimal_places=2)
    genre = models.ManyToManyField('Genre')  # Assuming a separate Genre model
    imdb_link = models.URLField()

# Assuming a separate Genre model for clarity and flexibility
class Genre(models.Model):
    name = models.CharField(max_length=100)
