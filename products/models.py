from django.db import models
from django.utils.text import slugify

def product_image_upload_to(instance, filename):
    return f"products/{instance.id or 'new'}/{filename}"

class Product(models.Model):
    name        = models.CharField(max_length=200)
    # ให้ null=True ชั่วคราว เพื่อให้เพิ่มคอลัมน์ได้โดยไม่ต้องกรอกค่าเดิม
    slug        = models.SlugField(max_length=220, unique=True, blank=True, null=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField(default=0)
    image       = models.ImageField(upload_to=product_image_upload_to, blank=True, null=True)
    description = models.TextField(blank=True)
    is_active   = models.BooleanField(default=True)
    
    slug        = models.SlugField(max_length=220, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
   
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # สร้าง slug อัตโนมัติถ้ายังไม่มี
        if not self.slug and self.name:
            base = slugify(self.name)
            slug = base or "product"
            i = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)
