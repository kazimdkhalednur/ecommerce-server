import random

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.utils.text import slugify

domain = Site.objects.get_current().domain


def generate_random_number(cls):
    random_number = random.randint(1_000_000_000, 9_999_999_999)

    if cls.objects.filter(id=random_number).exists():
        return generate_random_number(cls)

    return random_number


def generate_title_to_slug(cls, title, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(title)

    if cls.objects.filter(slug=slug).exists():
        new_slug = slugify(title) + "-" + str(random.randint(1_000_000, 9_999_999))
        return generate_title_to_slug(cls, title, new_slug=new_slug)

    return slug


def send_mail_to_product_owner_for_out_of_stack(instance):
    owner = instance.owner
    subject = "Out of Stack"
    body = (
        f"Hi {owner.get_full_name()},"
        + f"""Your product "{instance.title}" is out of stack."""
        + "So please update product quantity as soon as possible"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(
        subject, body, f"{domain} <{from_email}>", [owner.email]
    )
    msg.send(fail_silently=False)


def thumbnail_directory_path(instance, filename):
    extension = filename.split(".")[-1]
    filename = "thumbnail." + extension
    return f"{instance.id}/{filename}"


def photo_1_directory_path(instance, filename):
    extension = filename.split(".")[-1]
    filename = "photo_1." + extension
    return f"{instance.product.id}/{filename}"


def photo_2_directory_path(instance, filename):
    extension = filename.split(".")[-1]
    filename = "photo_1." + extension
    return f"{instance.product.id}/{filename}"


def photo_3_directory_path(instance, filename):
    extension = filename.split(".")[-1]
    filename = "photo_1." + extension
    return f"{instance.product.id}/{filename}"


def photo_4_directory_path(instance, filename):
    extension = filename.split(".")[-1]
    filename = "photo_1." + extension
    return f"{instance.product.id}/{filename}"


def photo_5_directory_path(instance, filename):
    extension = filename.split(".")[-1]
    filename = "photo_1." + extension
    return f"{instance.product.id}/{filename}"


def photo_6_directory_path(instance, filename):
    extension = filename.split(".")[-1]
    filename = "photo_1." + extension
    return f"{instance.product.id}/{filename}"


def photo_7_directory_path(instance, filename):
    extension = filename.split(".")[-1]
    filename = "photo_1." + extension
    return f"{instance.product.id}/{filename}"


def photo_8_directory_path(instance, filename):
    extension = filename.split(".")[-1]
    filename = "photo_1." + extension
    return f"{instance.product.id}/{filename}"


def photo_9_directory_path(instance, filename):
    extension = filename.split(".")[-1]
    filename = "photo_1." + extension
    return f"{instance.product.id}/{filename}"
