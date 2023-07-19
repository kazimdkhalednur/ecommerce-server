from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeManager

from accounts.models import User

from .managers import PublishedProductManager
from .utils import *


class CategoryManager(TreeManager):
    def viewable(self):
        queryset = self.get_queryset().filter(level=0)
        return queryset


class Category(MPTTModel):
    title = models.CharField(max_length=50)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="sub"
    )

    objects = CategoryManager()

    class MPTTMeta:
        order_insertion_by = ["title"]

    def __str__(self):
        if self.parent is not None:
            return f"{self.parent} -> {self.title}"
        return self.title


PRODUCT_ID_TYPE = (
    ("default", "Default"),
    ("isbn", "ISBN"),
    ("ean", "EAN"),
    ("gtin", "GTIN"),
    ("upc", "UPC"),
)

PRODUCT_STATUS = (
    ("draft", "Draft"),
    ("published", "Published"),
    ("out_of_stack", "Out of stack"),
)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.CharField(
        "Product ID",
        max_length=20,
        primary_key=True,
        unique=True,
        serialize=False,
        blank=True,
    )
    id_type = models.CharField(
        max_length=20, choices=PRODUCT_ID_TYPE, default="default"
    )
    title = models.CharField(max_length=500)
    slug = models.SlugField(blank=True, unique=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    quantity = models.PositiveIntegerField()
    description = RichTextField()
    status = models.CharField(max_length=20, choices=PRODUCT_STATUS, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True)

    published_objects = PublishedProductManager()
    objects = models.Manager()

    def __str__(self):
        return str(self.id)

    def clean(self):
        if self.owner.role != "seller":
            raise ValidationError({"owner": "User role must be Seller"})

    def save(self, *args, **kwargs):
        if self.owner.role != "seller":
            return ValueError("User role must be seller")

        if not self.id and self.id_type == "default":
            self.id = generate_random_number(Product)

        if not self.slug:
            self.slug = generate_title_to_slug(Product, self.title)

        super(Product, self).save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    thumbnail = models.ImageField(
        upload_to=thumbnail_directory_path, blank=True, null=True
    )
    image_1 = models.ImageField(upload_to=photo_1_directory_path, blank=True, null=True)
    image_2 = models.ImageField(upload_to=photo_2_directory_path, blank=True, null=True)
    image_3 = models.ImageField(upload_to=photo_3_directory_path, blank=True, null=True)
    image_4 = models.ImageField(upload_to=photo_4_directory_path, blank=True, null=True)
    image_5 = models.ImageField(upload_to=photo_5_directory_path, blank=True, null=True)
    image_6 = models.ImageField(upload_to=photo_6_directory_path, blank=True, null=True)
    image_7 = models.ImageField(upload_to=photo_7_directory_path, blank=True, null=True)
    image_8 = models.ImageField(upload_to=photo_8_directory_path, blank=True, null=True)
    image_9 = models.ImageField(upload_to=photo_9_directory_path, blank=True, null=True)

    def __str__(self):
        return self.product.id

    def delete(self, *args, **kwargs):
        self.thumbnail.delete()
        self.image_1.delete()
        self.image_2.delete()
        self.image_3.delete()
        self.image_4.delete()
        self.image_5.delete()
        self.image_6.delete()
        self.image_7.delete()
        self.image_8.delete()
        self.image_9.delete()

        super(ProductImage, self).delete(*args, **kwargs)


class ProductQuestionAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="qa")
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.product.id


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.user.email
