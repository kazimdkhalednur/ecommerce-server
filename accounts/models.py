import csv
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLE = (
    ("buyer", "Buyer"),
    ("seller", "Seller"),
)


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True, unique=True, serialize=False, editable=False, blank=True
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=USER_ROLE, default="buyer")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid4()
        super(User, self).save(*args, **kwargs)


class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    total_order = models.SmallIntegerField(default=0)
    total_purchase = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if self.user.role != "buyer":
            return ValueError("User role must be Buyer")
        super(BuyerProfile, self).save(*args, **kwargs)


class Address(models.Model):
    profile = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address_1 = models.CharField(max_length=300)
    address_2 = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name_plural = "addresses"

    def __str__(self):
        return self.profile.user.email


file = open(settings.BASE_DIR / "country_name.csv", "r")
countries_name = csv.reader(file)
COUNTRY_NAME = ([name[0], name[0]] for name in countries_name)


class SellerProfie(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nid = models.CharField("NID", max_length=20, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    shop_name = models.CharField(max_length=100, blank=True)
    shop_address = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=50, choices=COUNTRY_NAME, blank=True)
    revenue = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.user.role != "seller":
            return ValueError("User role must be Seller")
        super(SellerProfie, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.email
