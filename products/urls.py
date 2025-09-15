# products/urls.py
from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="list"),
    path("categories/", views.category_list, name="categories"),   # ✅ route categories

    # Admin
    path("admin/products/", views.admin_product_list, name="admin_product_list"),
    path("admin/products/create/", views.admin_product_create, name="admin_product_create"),
    path("admin/products/<int:pk>/edit/", views.admin_product_edit, name="admin_product_edit"),
    path("admin/products/<int:pk>/delete/", views.admin_product_delete, name="admin_product_delete"),
    path("admin/products/<int:pk>/toggle/", views.admin_product_toggle, name="admin_product_toggle"),
]
