from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
import logging

# Configure logging
logger = logging.getLogger(__name__)


@receiver(post_save, sender=Product)
def log_product_change(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Product created: {instance.title}")
    else:
        logger.info(f"Product updated: {instance.title}")
