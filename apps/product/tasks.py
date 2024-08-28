from __future__ import absolute_import, unicode_literals
import os
import logging

from celery import shared_task

from apps.product.utils import (
    extract_data_from_tag,
    clean_extracted_data,
    get_or_create_product,
)
from apps.product.models import PTFileEntry


logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def process_image_data(self, image_data, product_image_id):
    try:
        data = extract_data_from_tag(image_data)
        print(data)
        valid_data = clean_extracted_data(data, product_image_id)
        print(valid_data)
        product = get_or_create_product(valid_data)
        PTFileEntry.objects.create(product=product)
        logger.info("Product saved successfully.")
        logger.info(f"Product ID: {product}")
    except Exception as e:
        logger.error(f"Error processing image data: {e}")
        raise self.retry(exc=e)
