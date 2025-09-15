from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "stock", "image", "description", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class":"w-full border border-red-400 rounded-xl px-3 py-2"}),
            "price": forms.NumberInput(attrs={"class":"w-full border border-red-400 rounded-xl px-3 py-2", "step":"0.01", "min":"0"}),
            "stock": forms.NumberInput(attrs={"class":"w-full border border-red-400 rounded-xl px-3 py-2", "min":"0"}),
            "image": forms.ClearableFileInput(attrs={"class":"block w-full text-sm"}),
            "description": forms.Textarea(attrs={"class":"w-full border border-red-400 rounded-xl px-3 py-2", "rows":4}),
        }
