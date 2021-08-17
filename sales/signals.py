from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=models.Orders)
def udpdate_product_quantity(sender, instance, **kwargs):
    """Upadates the quantities afters a order is finished."""

    if instance.status == models.ORDERED:

        diff_quantity = instance.quantity
        product = instance.product
        product.quantity -= diff_quantity
        product.save()
