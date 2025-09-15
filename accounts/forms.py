# accounts/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

User = get_user_model()

_BASE = 'w-full border rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500'


# ===== ฟอร์มแก้ไขข้อมูลผู้ใช้ (ใช้ในหน้าโปรไฟล์) =====
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        label='ชื่อผู้ใช้ (Username)',
        max_length=150,
        widget=forms.TextInput(attrs={'class': _BASE, 'placeholder': 'ชื่อผู้ใช้'})
    )
    first_name = forms.CharField(
        required=False, label='ชื่อจริง',
        widget=forms.TextInput(attrs={'class': _BASE, 'placeholder': 'ชื่อจริง'})
    )
    last_name = forms.CharField(
        required=False, label='นามสกุล',
        widget=forms.TextInput(attrs={'class': _BASE, 'placeholder': 'นามสกุล'})
    )
    email = forms.EmailField(
        required=False, label='อีเมล',
        widget=forms.EmailInput(attrs={'class': _BASE, 'placeholder': 'อีเมล'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = (self.cleaned_data.get('username') or '').strip()
        qs = User.objects.filter(username__iexact=username)
        if self.user:
            qs = qs.exclude(pk=self.user.pk)
        if qs.exists():
            raise forms.ValidationError('มีชื่อผู้ใช้นี้แล้ว กรุณาใช้ชื่ออื่น')
        return username

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip()
        if not email:
            return email
        qs = User.objects.filter(email__iexact=email)
        if self.user:
            qs = qs.exclude(pk=self.user.pk)
        if qs.exists():
            raise forms.ValidationError('อีเมลนี้ถูกใช้แล้ว')
        return email


# ===== ฟอร์มโปรไฟล์ (โทร/ที่อยู่/รูป) =====
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone', 'address', 'image']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': _BASE, 'placeholder': 'ชื่อ-นามสกุล'
            }),
            'phone': forms.TextInput(attrs={
                'class': _BASE, 'placeholder': 'เบอร์โทรศัพท์'
            }),
            'address': forms.Textarea(attrs={
                'rows': 3, 'class': _BASE, 'placeholder': 'ที่อยู่'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:bg-red-600 file:text-white hover:file:bg-red-700'
            }),
        }


# ===== ฟอร์มสมัครสมาชิก (มีชื่อจริง/นามสกุลด้วย) =====
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True, label="ชื่อจริง",
        widget=forms.TextInput(attrs={'class': _BASE, 'placeholder': 'ชื่อจริง'})
    )
    last_name = forms.CharField(
        required=True, label="นามสกุล",
        widget=forms.TextInput(attrs={'class': _BASE, 'placeholder': 'นามสกุล'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': _BASE, 'placeholder': 'อีเมล'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': _BASE, 'placeholder': 'ชื่อผู้ใช้'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': _BASE, 'placeholder': 'รหัสผ่าน'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': _BASE, 'placeholder': 'ยืนยันรหัสผ่าน'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    # ตรวจซ้ำให้ชัดเจน (เผื่อ template ไม่โชว์ error ของ default validators)
    def clean_username(self):
        username = (self.cleaned_data.get('username') or '').strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('มีชื่อผู้ใช้นี้แล้ว กรุณาใช้ชื่ออื่น')
        return username

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('อีเมลนี้ถูกใช้แล้ว')
        return email
