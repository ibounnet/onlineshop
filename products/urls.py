# products/urls.py
from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="list"),
    path("categories/", views.category_list, name="categories"),   # ✅ route categories
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:product_id>/", views.cart_update, name="cart_update"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
]
