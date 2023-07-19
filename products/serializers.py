from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.serializers import UserDataSerializer

from .models import *


class CategorySerializer(ModelSerializer):
    sub_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "title", "sub_category"]
        depth = 1

    def get_sub_category(self, obj):
        return CategorySerializer(obj.get_children(), many=True).data


class SuperCategorySerializer(ModelSerializer):
    sup_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "title", "sup_category"]
        depth = 1

    def get_sup_category(self, obj):
        if not obj.is_root_node():
            return SuperCategorySerializer(obj.parent).data
        return None


class ProductCreateSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ["owner", "published_at", "created_at"]


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ["id", "product"]


class ProductSerializer(ModelSerializer):
    category = SuperCategorySerializer()
    images = ProductImageSerializer()

    class Meta:
        model = Product
        exclude = ["owner", "published_at", "created_at"]
        depth = 1


class CartSerializer(ModelSerializer):
    user = UserDataSerializer(required=False)
    product = ProductSerializer(required=False)

    class Meta:
        model = Cart
        fields = "__all__"
        depth = 1
