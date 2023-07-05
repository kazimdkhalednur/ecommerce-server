from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BuyerProfile, SellerProfie, User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        if instance.role == "buyer":
            BuyerProfile.objects.create(user=instance)
        elif instance.role == "seller":
            SellerProfie.objects.create(user=instance)
