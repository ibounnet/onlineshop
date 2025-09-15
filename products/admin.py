from django.contrib import admin
from django.utils.html import format_html
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "price", "stock", "is_active", "updated_at")
    list_editable = ("price", "stock", "is_active")
    search_fields = ("name", "description", "slug")
    list_filter = ("is_active", "created_at")
    readonly_fields = ("created_at", "updated_at", "image_preview")
    prepopulated_fields = {"slug": ("name",)}  # ถ้าต้องการให้กรอกเองก็ลบออก
    fieldsets = (
        ("ข้อมูลหลัก", {"fields": ("name", "slug", "price", "stock", "is_active")}),
        ("รูปภาพ",     {"fields": ("image", "image_preview")}),
        ("รายละเอียด", {"fields": ("description",)}),
        ("ระบบ",       {"fields": ("created_at", "updated_at")}),
    )

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:6px;border:1px solid #eee;" />', obj.image.url)
        return "—"
    thumb.short_description = "รูป"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:200px;border:1px solid #eee;border-radius:8px;" />', obj.image.url)
        return "—"
    image_preview.short_description = "พรีวิว"
