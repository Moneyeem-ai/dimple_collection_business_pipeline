from __future__ import absolute_import, unicode_literals
import os
import logging

from celery import shared_task

from apps.product.utils import extract_data_from_tag
from apps.product.models import Product, ProductTagImage, PTFileEntry
from apps.department.models import SubCategory, Department, Category


logger = logging.getLogger(__name__)


@shared_task()
def process_image_data(image_data, product_image_id):
    # Task to process image data
    try:
        data = extract_data_from_tag(image_data)
        
        valid_keys = [field.name for field in Product._meta.get_fields()]
        valid_keys.remove("department")
        valid_keys.append("department_id")
        valid_keys.remove("brand")
        valid_keys.append("brand_id")
        valid_data = {key: value for key, value in data.items() if key in valid_keys}
        valid_data["metadata"] = data
        valid_data["product_images"] = ProductTagImage.objects.get(id=product_image_id)
        department, created = Department.objects.get_or_create(department_name = "None")
        valid_data["category"], created = Category.objects.get_or_create(category_name="None", department=department)
        valid_data["subcategory"], created = SubCategory.objects.get_or_create(subcategory_name="None", category=valid_data["category"])
        print(valid_data["category"])
        print(valid_data["subcategory"])
        product = Product.objects.create(**valid_data)
        logger.info(f"product: {product}")
        logger.info(str(product.id is None))
        
        if product.id is not None:
            pt_file_data = PTFileEntry.objects.create(product=product)

        logger.info("Product saved successfully.")
        logger.info(f"Product ID: {product}")
    except Exception as e:
        logger.error(f"Error processing image data: {e}")
