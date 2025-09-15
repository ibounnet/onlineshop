from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Product
from django.contrib import messages
from django.shortcuts import render, redirect

from django.shortcuts import render
from .models import Product
from .forms import ProductForm
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:12]
    return render(request, "products/home.html", {"products": products})

@login_required(login_url='login')  # << ตรงนี้สำคัญ
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/home.html', {'products': products})

# ---------- helpers (session cart) ----------
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
    cart = _get_cart(request.session)
    items = []
    for pid, data in cart.items():
        price = float(data["price"]); qty = int(data["qty"])
        items.append({"pid": pid, "name": data["name"], "price": price, "qty": qty, "subtotal": price * qty})
    total_qty, total_price = _totals(request.session)
    return render(request, "products/cart.html", {"items": items, "total_qty": total_qty, "total_price": total_price})

@login_required
def cart_add(request, product_id):
    if request.method == "POST":
        name = request.POST.get("name", f"Product {product_id}")
        price = float(request.POST.get("price", "0"))
        qty = max(1, int(request.POST.get("qty", "1") or 1))

        cart = _get_cart(request.session)
        pid = str(product_id)
        item = cart.get(pid, {"name": name, "price": price, "qty": 0})
        item["qty"] += qty
        item["name"] = name
        item["price"] = price
        cart[pid] = item
        _save_cart(request.session, cart)
        messages.success(request, "เพิ่มสินค้าลงตะกร้าแล้ว")
    return redirect("cart_detail")

@login_required
def cart_update(request, product_id):
    if request.method == "POST":
        qty = max(1, int(request.POST.get("qty", "1") or 1))
        cart = _get_cart(request.session)
        pid = str(product_id)
        if pid in cart:
            cart[pid]["qty"] = qty
            _save_cart(request.session, cart)
            messages.success(request, "อัปเดตจำนวนแล้ว")
    return redirect("cart_detail")

@login_required
def cart_remove(request, product_id):
    if request.method == "POST":
        cart = _get_cart(request.session)
        pid = str(product_id)
        if pid in cart:
            del cart[pid]
            _save_cart(request.session, cart)
            messages.success(request, "ลบสินค้าแล้ว")
    return redirect("cart_detail")

from django.shortcuts import render

def home(request):
    return render(request, 'products/home.html')

def category_list(request):
    # ดึงหมวดหมู่จริงในภายหลัง ตอนนี้ให้หน้าแสดงผลได้ก่อน
    return render(request, 'products/categories.html')

def cart(request):
    return render(request, 'products/cart.html')

@staff_member_required
def admin_product_list(request):
    q = request.GET.get("q", "").strip()
    qs = Product.objects.all().order_by("-updated_at")
    if q:
        qs = qs.filter(name__icontains=q)
    return render(request, "products/admin/list.html", {"products": qs, "q": q})

# ====== Admin: Create ======
@staff_member_required
def admin_product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save()  # slug จะถูก generate ใน model.save()
            messages.success(request, f"เพิ่มสินค้า “{p.name}” แล้ว")
            return redirect("admin_product_list")
        messages.error(request, "กรุณาตรวจสอบข้อมูลที่กรอก")
    else:
        form = ProductForm()
    return render(request, "products/admin/form.html", {"form": form, "mode": "create"})

# ====== Admin: Edit ======
@staff_member_required
def admin_product_edit(request, pk):
    p = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=p)
        if form.is_valid():
            p = form.save()
            messages.success(request, f"บันทึกสินค้า “{p.name}” แล้ว")
            return redirect("admin_product_list")
        messages.error(request, "กรุณาตรวจสอบข้อมูลที่กรอก")
    else:
        form = ProductForm(instance=p)
    return render(request, "products/admin/form.html", {"form": form, "mode": "edit", "product": p})

# ====== Admin: Delete ======
@staff_member_required
def admin_product_delete(request, pk):
    p = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        name = p.name
        p.delete()
        messages.success(request, f"ลบสินค้า “{name}” แล้ว")
        return redirect("admin_product_list")
    return render(request, "products/admin/delete_confirm.html", {"product": p})

# ====== Admin: Toggle Active/Inactive ======
@staff_member_required
def admin_product_toggle(request, pk):
    p = get_object_or_404(Product, pk=pk)
    p.is_active = not p.is_active
    p.save()
    messages.success(request, f"อัปเดตสถานะ “{p.name}” เป็น {'แสดง' if p.is_active else 'ซ่อน'} แล้ว")
    return redirect("admin_product_list")