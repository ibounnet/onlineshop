
def cart_badge(request):
    cart = request.session.get("cart", {})
    total_qty = sum(item.get("qty", 0) for item in cart.values())
    return {"cart_qty": total_qty}
