from django.urls import path

from .views import *

app_name = "products"
urlpatterns = [
    path("cart/<str:slug>/", CartView.as_view(), name="cart"),
    path("category/", CategoriesView.as_view(), name="category"),
    path("product-id-type/", ProductIDTypeView.as_view(), name="id_type"),
    path("products/my/", SellerProductsView.as_view(), name="seller_list"),
    path("products/my/<str:slug>/", SellerProductView.as_view(), name="seller_detail"),
    path("", ProductsView.as_view(), name="list"),
    path("<str:slug>/", ProductView.as_view(), name="detail"),
]
