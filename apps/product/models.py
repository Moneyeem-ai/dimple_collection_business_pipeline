import hashlib

from django.db import models


class ProductImages(models.Model):
    product_image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    tag_image = models.ImageField(upload_to='tag_images/', null=True, blank=True)


class ProcessingStatus(models.TextChoices):
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'


class Product(models.Model):
    department = models.CharField(max_length=64, null=True, blank=True)
    category = models.CharField(max_length=64, null=True, blank=True)
    subcategory = models.CharField(max_length=64, null=True, blank=True)
    brand = models.CharField(max_length=64, null=True, blank=True)
    article_number = models.CharField(max_length=128, null=True, blank=True)
    product_images = models.ForeignKey(ProductImages, null=True, blank=True, on_delete=models.CASCADE)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    processed = models.CharField(max_length=20, default=ProcessingStatus.PENDING, choices=ProcessingStatus.choices)
    hash_value = models.CharField(max_length=64, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.department or not self.brand or not self.article_number:
            self.hash_value = None
        else:
            # Calculate hash using SHA256
            hash_string = f"{self.department}{self.brand}{self.article_number}"
            hash_value = hashlib.sha256(hash_string.encode()).hexdigest()
            self.hash_value = hash_value

        existing_entry = Product.objects.filter(hash_value=hash_value).first()

        if existing_entry:
            return existing_entry.id
        else:
            super().save(*args, **kwargs)
            return self.id
    

class PTStatus(models.TextChoices):
    PROCESSING = 'PROCESSING'
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'


# actual PT file data is in this model
class PTFileData(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=64, default=PTStatus.PROCESSING, choices=PTStatus.choices)
    size = models.CharField(max_length=128, null=True, blank=True)
    quantity = models.IntegerField()
    color = models.CharField(max_length=64, null=True, blank=True)
    wsp = models.CharField(max_length=128, null=True, blank=True)
    mrp = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.quantity


class ProductBarcode(models.Model):
    product = models.ForeignKey(PTFileData, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=128, unique=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return self.barcode
