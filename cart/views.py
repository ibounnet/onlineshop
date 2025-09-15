# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product

@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related("product").all()
    total_qty = sum(i.quantity for i in items)
    total_price = sum(i.subtotal for i in items)
    return render(request, "cart/cart.html", {
        "items": items,
        "total_qty": total_qty,
        "total_price": total_price,
    })

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.save()
    messages.success(request, f"เพิ่ม {product.name} ลงตะกร้าแล้ว")
    return redirect("cart:cart_detail")

@login_required
def cart_update(request, product_id):
    if request.method == "POST":
        qty = max(1, int(request.POST.get("qty", "1") or 1))
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        item.quantity = qty
        item.save()
        messages.success(request, "อัปเดตจำนวนแล้ว")
    return redirect("cart:cart_detail")

@login_required
def cart_remove(request, product_id):
    if request.method == "POST":
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        item.delete()
        messages.success(request, "ลบสินค้าแล้ว")
    return redirect("cart:cart_detail")
