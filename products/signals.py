from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Product
from .utils import send_mail_to_product_owner_for_out_of_stack


@receiver(post_save, sender=Product)
def send_mail_for_out_of_stack(sender, instance, created, *args, **kwargs):
    if instance.quantity == 0 and instance.status == "published":
        instance.status = "out_of_stack"
        instance.published_at = None
        instance.save()
        send_mail_to_product_owner_for_out_of_stack(instance)


@receiver(pre_save, sender=Product)
def update_published_time(sender, instance, *args, **kwargs):
    if instance.status == "published" and not instance.published_at:
        instance.published_at = timezone.now()
