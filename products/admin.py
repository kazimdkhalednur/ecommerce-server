from django.contrib import admin

from .models import Cart, Category, Product, ProductImage


class ProductImageInline(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    date_hierarchy = "published_at"
    inlines = [
        ProductImageInline,
    ]


admin.site.register(Category)
admin.site.register(Cart)
