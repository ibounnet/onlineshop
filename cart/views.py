from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product

def cart_detail(request):
    cart = request.session.get("cart", {})
    items = []
    total_qty = 0
    total_price = 0

    for pid, data in cart.items():
        price = float(data["price"])
        qty = int(data["qty"])
        subtotal = price * qty
        total_qty += qty
        total_price += subtotal
        items.append({
            "pid": pid,
            "name": data["name"],
            "price": price,
            "qty": qty,
            "subtotal": subtotal,
        })

    return render(request, "cart/cart.html", {
        "items": items,
        "total_qty": total_qty,
        "total_price": total_price
    })

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    item.quantity += 1
    item.save()
    messages.success(request, f"เพิ่ม {product.name} ลงตะกร้าแล้ว")
    return redirect("cart:cart_detail")

@login_required
def cart_update(request, product_id):
    if request.method == "POST":
        qty = max(1, int(request.POST.get("qty", "1") or 1))
        cart = request.session.get("cart", {})
        pid = str(product_id)
        if pid in cart:
            cart[pid]["qty"] = qty
            request.session["cart"] = cart
            request.session.modified = True
            messages.success(request, "อัปเดตจำนวนแล้ว")
    # แก้จาก redirect("home") → redirect ไปหน้า cart
    return redirect("cart:cart_detail")


@login_required
def cart_remove(request, product_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        pid = str(product_id)
        if pid in cart:
            del cart[pid]
            request.session["cart"] = cart
            request.session.modified = True
            messages.success(request, "ลบสินค้าแล้ว")
    # แก้จาก redirect("home") → redirect ไปหน้า cart
    return redirect("cart:cart_detail")