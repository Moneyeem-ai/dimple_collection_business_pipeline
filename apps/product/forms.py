from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["department", "category", "subcategory", "brand", "color", "article_number", "size", "wsp", "mrp"]
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'subcategory': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'article_number': forms.TextInput(attrs={'class': 'form-control'}),
            'size': forms.NumberInput(attrs={'class': 'form-control'}),
            'wsp': forms.TextInput(attrs={'class': 'form-control'}),
            'mrp': forms.TextInput(attrs={'class': 'form-control'}),
        }
