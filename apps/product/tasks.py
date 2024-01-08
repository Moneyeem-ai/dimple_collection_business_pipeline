from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings
from apps.product.utils import extract_data_from_tag
from apps.product.models import Product
import os
import logging

logger = logging.getLogger(__name__)

@shared_task()
def process_image_data(image_data):
    # Task to process image data
    try:
        data = extract_data_from_tag(image_data)
        print("this one is data",data)
        product = Product.objects.create()
        for key, value in data.items():
            setattr(product, key, value)
        product.metadata = data
        product.save()
        logger.info("Product saved successfully.")
        logger.info(f"Product ID: {product.id}")
    except Exception as e:
        logger.error(f"Error processing image data: {e}")
    
    
