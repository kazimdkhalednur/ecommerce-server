import json

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, Response

from utils.permissions import IsSeller

from .models import *
from .serializers import *


class CategoriesView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.viewable()


class ProductsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.published_objects.all()


class ProductView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.published_objects.all()
    lookup_field = "slug"


class ProductIDTypeView(APIView):
    permission_classes = [IsSeller]

    def get(self, request, format=None):
        product_id_type = []
        for id_type in PRODUCT_ID_TYPE:
            product_id_type.append({"value": id_type[0], "human_read": id_type[1]})
        return Response(product_id_type, status=status.HTTP_200_OK)


class SellerProductsView(APIView):
    permission_classes = [IsSeller]

    def get(self, request, format=None):
        my_products = Product.objects.filter(owner=self.request.user)
        serializer = ProductSerializer(my_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ProductCreateSerializer(data=request.data)

        if serializer.is_valid():
            product = serializer.save(owner=request.user)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellerProductView(APIView):
    permission_classes = [IsSeller]

    def get(self, request, slug, format=None):
        my_product = get_object_or_404(Product, slug=slug, owner=request.user)
        serializer = ProductSerializer(my_product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug, format=None):
        my_product = get_object_or_404(Product, slug=slug, owner=request.user)
        serializer = ProductCreateSerializer(my_product, data=request.data)

        if serializer.is_valid():
            product = serializer.save()
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, slug, format=None):
        my_product = get_object_or_404(Product, slug=slug, owner=request.user)
        serializer = ProductCreateSerializer(
            my_product, data=request.data, partial=True
        )

        if serializer.is_valid():
            product = serializer.save()
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        my_product = get_object_or_404(Product, slug=slug, owner=request.user)
        my_product.delete()
        return Response(
            {"success": "The product is deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class CartView(APIView):
    def get(self, request, format=None):
        cart = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, slug, format=None):
        product = get_object_or_404(Product, slug=slug)
        serializer = CartSerializer(data=request.data)

        if serializer.is_valid():
            if not Cart.objects.filter(user=request.user, product=product).exists():
                serializer.save(product=product, user=request.user)
            else:
                cart = Cart.objects.get(user=request.user, product=product)
                cart.quantity += serializer.data["quantity"]
                cart.save()
                serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
