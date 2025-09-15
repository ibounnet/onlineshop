# accounts/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.forms import (
    ProfileForm,
    UserUpdateForm,
    UserRegisterForm,   # ฟอร์มสมัครสมาชิกที่มี first_name/last_name
)
from .models import Profile

User = get_user_model()


def _username_from_identifier(identifier: str) -> str:
    """
    แปลง identifier ที่ผู้ใช้กรอกให้เป็น username สำหรับ authenticate:
    - ถ้ามี '@' ให้ถือว่าเป็นอีเมล แล้วค้นหา User เพื่อดึง username
    - ถ้าไม่ใช่อีเมล ใช้เป็น username ตรง ๆ
    """
    identifier = (identifier or "").strip()
    if "@" in identifier:
        try:
            user = User.objects.get(email__iexact=identifier)
            return user.username
        except User.DoesNotExist:
            return identifier
    return identifier


def user_login(request):
    if request.method == "POST":
        identifier = request.POST.get("username") or request.POST.get("email")
        password = request.POST.get("password")
        username = _username_from_identifier(identifier)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            nxt = request.GET.get("next") or request.POST.get("next")
            return redirect(nxt) if nxt else redirect(reverse("home"))

        messages.error(request, "ชื่อผู้ใช้/อีเมล หรือรหัสผ่านไม่ถูกต้อง")
    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    return redirect(reverse("home"))


def register(request):
    """
    สมัครสมาชิก: ใช้ UserRegisterForm ที่มี first_name/last_name ด้วย
    ไม่ส่ง message.success เพื่อไม่ให้ไปโผล่ที่หน้าถัดไปโดยไม่ตั้งใจ
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # ฟิลด์หลักอยู่ในฟอร์มแล้ว (username, email, first_name, last_name)
            user.save()
            Profile.objects.get_or_create(user=user)  # เผื่อไม่มี signal
            return redirect("login")
        else:
            messages.error(request, "กรุณาตรวจสอบข้อมูลที่กรอก")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, "accounts/profile.html", {"profile": profile_obj})


@login_required
def profile_edit(request):
    """
    แก้โปรไฟล์: แก้ได้ทั้ง User (username/first_name/last_name/email)
    และ Profile (full_name/phone/address/image)
    """
    profile = request.user.profile  # มีจาก signal แล้ว

    if request.method == "POST":
        uform = UserUpdateForm(request.POST, instance=request.user, user=request.user)
        pform = ProfileForm(request.POST, request.FILES, instance=profile)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, "บันทึกโปรไฟล์แล้ว")
            return redirect("profile")
        else:
            messages.error(request, "กรุณาตรวจสอบข้อมูลที่กรอก")
    else:
        uform = UserUpdateForm(instance=request.user, user=request.user)
        pform = ProfileForm(instance=profile)

    return render(request, "accounts/profile_edit.html", {
        "uform": uform,
        "form": pform,     # ProfileForm
        "profile": profile
    })


@login_required
def profile_delete_confirm(request):
    if request.method == "POST":
        request.user.delete()   # ลบ User จะพ่วงลบ Profile (on_delete=CASCADE)
        messages.success(request, "ลบบัญชีแล้ว")
        return redirect("home")
    return render(request, "accounts/profile_delete_confirm.html")
