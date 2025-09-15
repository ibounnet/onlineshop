# accounts/models.py
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def profile_image_upload_to(instance, filename: str) -> str:
    return f"profiles/user_{instance.user_id}/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    full_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    image = models.ImageField(
        upload_to=profile_image_upload_to,  # ใช้ฟังก์ชันด้านบน
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


    # ใช้ใน template ได้ง่ายขึ้น โดยไม่ต้องเขียน if/else ใน {{ ... }}
    @property
    def image_url(self) -> str:
        try:
            return self.image.url if self.image else ""
        except ValueError:
            # กรณีไฟล์หาย/เส้นทางผิด
            return ""

    def __str__(self) -> str:
        return f"Profile({self.user.username})"

    class Meta:
        verbose_name = "โปรไฟล์"
        verbose_name_plural = "โปรไฟล์"
        ordering = ["-updated_at"]


# --- Signals: สร้างโปรไฟล์ให้ผู้ใช้ใหม่อัตโนมัติ และ ensure มีโปรไฟล์เสมอ ---

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_when_user_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile_when_user_saved(sender, instance, **kwargs):
    # เผื่อกรณีโปรไฟล์หายไป ให้สร้างใหม่
    profile, _ = Profile.objects.get_or_create(user=instance)
    # บันทึกเพื่ออัปเดต timestamp หรือ trigger logic อื่น (ถ้ามี)
    profile.save()
