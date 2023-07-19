from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import *


class ProductModelTests(TestCase):
    def setUp(self):
        self.seller1 = User.objects.create_user(
            "seller1", email="seller1@email.com", password="1234@#$%", role="seller"
        )
        self.seller2 = User.objects.create_user(
            "seller2", email="seller2@email.com", password="1234@#$%", role="seller"
        )
        self.category = Category.objects.create(title="food")

    def test_product_create(self):
        product = Product.objects.create(
            owner=self.seller1,
            category=self.category,
            title="title",
            price=23.6,
            quantity=23,
            description="this is description",
        )

        self.assertEqual(Product.objects.count(), 1)
        self.assertNotEqual(Product.published_objects.count(), 1)
        self.assertEqual(product.id_type, "default")
        self.assertEqual(product.status, "draft")

    def test_unique_slug(self):
        product1 = Product.objects.create(
            owner=self.seller1,
            category=self.category,
            title="title",
            price=23.6,
            quantity=23,
            description="this is description",
        )
        product2 = Product.objects.create(
            owner=self.seller2,
            category=self.category,
            title="title",
            price=23.6,
            quantity=23,
            description="this is description",
        )

        self.assertEqual(product1.slug, slugify("title"))
        self.assertNotEqual(product2.slug, slugify("title"))


class ProductAPIViewTests(APITestCase):
    login_url = reverse("accounts:token")

    def setUp(self):
        self.password = "1234@#$%"
        self.buyer = User.objects.create_user(
            "buyer", email="buyer@email.com", password=self.password
        )
        self.seller1 = User.objects.create_user(
            "seller1", email="seller1@email.com", password=self.password, role="seller"
        )
        self.seller2 = User.objects.create_user(
            "seller2", email="seller2@email.com", password=self.password, role="seller"
        )
        self.category = Category.objects.create(title="food")
        self.product1 = Product.objects.create(
            owner=self.seller1,
            category=self.category,
            title="title",
            price=23.6,
            quantity=23,
            description="this is description",
            status="published",
        )
        self.product2 = Product.objects.create(
            owner=self.seller1,
            category=self.category,
            title="title2",
            price=23.6,
            quantity=23,
            description="this is description",
            status="published",
        )
        self.product3 = Product.objects.create(
            owner=self.seller2,
            category=self.category,
            title="title3",
            price=23.6,
            quantity=23,
            description="this is description",
            status="published",
        )

    def login_buyer(self):
        data = {"email": self.buyer.email, "password": self.password}
        response = self.client.post(self.login_url, data, format="json")
        access = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)

    def login_seller1(self):
        data = {"email": self.seller1.email, "password": self.password}
        response = self.client.post(self.login_url, data, format="json")
        access = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)

    def login_seller2(self):
        data = {"email": self.seller2.email, "password": self.password}
        response = self.client.post(self.login_url, data, format="json")
        access = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)

    def test_product_list(self):
        response = self.client.get(reverse("products:list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Product.published_objects.all().count())

    def test_product_detail(self):
        response = self.client.get(
            reverse("products:detail", kwargs={"slug": self.product1.slug})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.product1.title)
        self.assertEqual(response.data["status"], self.product1.status)

    def test_seller_own_product_list(self):
        self.login_seller1()

        response = self.client.get(reverse("products:seller_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            Product.published_objects.filter(owner=self.seller1).count(),
        )

    def test_seller_own_product_detail(self):
        self.login_seller2()

        response = self.client.get(
            reverse("products:seller_detail", kwargs={"slug": self.product3.slug})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.product3.title)

    def test_other_seller_product_detail(self):
        self.login_seller2()

        response = self.client.get(
            reverse("products:seller_detail", kwargs={"slug": self.product1.slug})
        )

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
