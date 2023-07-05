from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Address, BuyerProfile, SellerProfie, User

admin.site.register(Address)
admin.site.register(BuyerProfile)
admin.site.register(SellerProfie)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ["email", "username"]
    fieldsets = (
        *UserAdmin.fieldsets,
        ("User Role", {"fields": ("role",)}),
    )
