from __future__ import absolute_import, unicode_literals
import os
import logging

from celery import shared_task

from apps.product.utils import extract_data_from_tag
from apps.product.models import Product, ProductTagImage, PTFileEntry


logger = logging.getLogger(__name__)


@shared_task()
def process_image_data(image_data, product_image_id):
    # Task to process image data
    try:
        data = extract_data_from_tag(image_data)
        
        valid_keys = [field.name for field in Product._meta.get_fields()]
        valid_keys.remove("department")
        valid_keys.append("department_id")
        valid_data = {key: value for key, value in data.items() if key in valid_keys}
        valid_data["metadata"] = data
        valid_data["product_images"] = ProductTagImage.objects.get(id=product_image_id)
        product = Product.objects.create(**valid_data)
        logger.info(f"product: {product}")
        logger.info(str(product.id is None))
        if product.id is not None:
            pt_file_data = PTFileEntry.objects.create(product=product)

        logger.info("Product saved successfully.")
        logger.info(f"Product ID: {product}")
    except Exception as e:
        logger.error(f"Error processing image data: {e}")
