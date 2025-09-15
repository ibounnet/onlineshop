from django.contrib import admin
from django.urls import path, include
from orders import settings
from products import views as product_views
from accounts import views as account_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static   # <— เพิ่มบรรทัดนี้

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", product_views.product_list, name="home"),
    path('', include('products.urls')),        # หน้า home, categories, cart ฯลฯ
    path('', include('accounts.urls')), 

    path("login/", account_views.user_login, name="login"),
    path("register/", account_views.register, name="register"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),

    path("accounts/", include("accounts.urls")),
    path("cart/", include("cart.urls", namespace="cart")),
    path("products/", include("products.urls", namespace="products")),
    path("cart/add/<int:product_id>/", product_views.cart_add, name="cart_add"),
    path("cart/update/<int:product_id>/", product_views.cart_update, name="cart_update"),
    path("cart/remove/<int:product_id>/", product_views.cart_remove, name="cart_remove"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # type: ignore