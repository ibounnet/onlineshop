from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile
admin.site.unregister(User)

# แล้วลงทะเบียนใหม่แบบปรับแต่ง
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')  # เพิ่มคอลัมน์ที่ต้องการ

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'updated_at')
    search_fields = ('user__username', 'full_name', 'phone')