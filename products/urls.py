from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("categories/", views.category_list, name="categories"),
    path("cart/", views.cart, name="cart"),
    

    # ===== Admin (frontend) =====
    path("dashboard/products/", views.admin_product_list, name="admin_product_list"),
    path("dashboard/products/create/", views.admin_product_create, name="admin_product_create"),
    path("dashboard/products/<int:pk>/edit/", views.admin_product_edit, name="admin_product_edit"),
    path("dashboard/products/<int:pk>/delete/", views.admin_product_delete, name="admin_product_delete"),
    path("dashboard/products/<int:pk>/toggle/", views.admin_product_toggle, name="admin_product_toggle"),
]
