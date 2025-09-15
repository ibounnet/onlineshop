from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Product
from .forms import ProductForm

# ---------- Public Views ----------

def home(request):
    """หน้าแรก: แสดงสินค้าที่ active"""
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:12]
    return render(request, "products/home.html", {"products": products})

@login_required(login_url='login')
def product_list(request):
    """แสดงรายการสินค้า (ต้องล็อกอิน)"""
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})


# ---------- Cart Helpers (session) ----------
def _get_cart(session):
    return session.setdefault("cart", {})  # {"pid": {"name": "...", "price": 100.0, "qty": 2}}

def _save_cart(session, cart):
    session["cart"] = cart
    session.modified = True

def _totals(session):
    cart = _get_cart(session)
    total_qty = sum(i["qty"] for i in cart.values())
    total_price = sum(i["qty"] * float(i["price"]) for i in cart.values())
    return total_qty, total_price
# -------------------------------------------

@login_required
def cart_detail(request):
    """ดูรายละเอียดตะกร้า"""
    cart = _get_cart(request.session)
    items = []
    for pid, data in cart.items():
        price = float(data["price"])
        qty = int(data["qty"])
        items.append({
            "pid": pid,
            "name": data["name"],
            "price": price,
            "qty": qty,
            "subtotal": price * qty
        })
    total_qty, total_price = _totals(request.session)
    return render(request, "products/cart.html", {
        "items": items,
        "total_qty": total_qty,
        "total_price": total_price
    })

@login_required
def cart_add(request, product_id):
    """เพิ่มสินค้าเข้าตะกร้า"""
    product = get_object_or_404(Product, pk=product_id)
    cart = _get_cart(request.session)
    pid = str(product_id)

    item = cart.get(pid, {"name": product.name, "price": float(product.price), "qty": 0})
    item["qty"] += 1
    cart[pid] = item

    _save_cart(request.session, cart)
    messages.success(request, f"เพิ่ม {product.name} ลงตะกร้าแล้ว")
    return redirect("products:cart_detail")

@login_required
def cart_update(request, product_id):
    """อัปเดตจำนวนสินค้าในตะกร้า"""
    if request.method == "POST":
        qty = max(1, int(request.POST.get("qty", "1") or 1))
        cart = _get_cart(request.session)
        pid = str(product_id)
        if pid in cart:
            cart[pid]["qty"] = qty
            _save_cart(request.session, cart)
            messages.success(request, "อัปเดตจำนวนแล้ว")
    return redirect("products:cart_detail")

@login_required
def cart_remove(request, product_id):
    """ลบสินค้าออกจากตะกร้า"""
    cart = _get_cart(request.session)
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
        _save_cart(request.session, cart)
        messages.success(request, "ลบสินค้าแล้ว")
    return redirect("products:cart_detail")


# ---------- Category ----------
def category_list(request):
    # TODO: ดึงหมวดหมู่จริงในภายหลัง
    return render(request, 'products/categories.html')


# ---------- Admin CRUD ----------
@staff_member_required
def admin_product_list(request):
    q = request.GET.get("q", "").strip()
    qs = Product.objects.all().order_by("-updated_at")
    if q:
        qs = qs.filter(name__icontains=q)
    return render(request, "products/admin/list.html", {"products": qs, "q": q})

@staff_member_required
def admin_product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save()
            messages.success(request, f"เพิ่มสินค้า “{p.name}” แล้ว")
            return redirect("products:admin_product_list")
        messages.error(request, "กรุณาตรวจสอบข้อมูลที่กรอก")
    else:
        form = ProductForm()
    return render(request, "products/admin/form.html", {"form": form, "mode": "create"})

@staff_member_required
def admin_product_edit(request, pk):
    p = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=p)
        if form.is_valid():
            p = form.save()
            messages.success(request, f"บันทึกสินค้า “{p.name}” แล้ว")
            return redirect("products:admin_product_list")
        messages.error(request, "กรุณาตรวจสอบข้อมูลที่กรอก")
    else:
        form = ProductForm(instance=p)
    return render(request, "products/admin/form.html", {"form": form, "mode": "edit", "product": p})

@staff_member_required
def admin_product_delete(request, pk):
    p = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        name = p.name
        p.delete()
        messages.success(request, f"ลบสินค้า “{name}” แล้ว")
        return redirect("products:admin_product_list")
    return render(request, "products/admin/delete_confirm.html", {"product": p})

@staff_member_required
def admin_product_toggle(request, pk):
    p = get_object_or_404(Product, pk=pk)
    p.is_active = not p.is_active
    p.save()
    messages.success(request, f"อัปเดตสถานะ “{p.name}” เป็น {'แสดง' if p.is_active else 'ซ่อน'} แล้ว")
    return redirect("products:admin_product_list")
