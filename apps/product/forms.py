from django import forms
from django.forms import inlineformset_factory

from .models import Product, PTFileEntry


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["department", "category", "subcategory", "brand", "article_number"]
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'subcategory': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'article_number': forms.TextInput(attrs={'class': 'form-control'})
        }


PTFileEntryForm = forms.modelform_factory(
    PTFileEntry,
    fields=('product', 'status', 'size', 'quantity', 'color', 'wsp', 'mrp')
)

PTFileEntryFormSet = inlineformset_factory(
    Product,
    PTFileEntry,
    form=PTFileEntryForm,
    extra=1,  # Set to the number of empty forms you want to display initially
    can_delete=True
)
