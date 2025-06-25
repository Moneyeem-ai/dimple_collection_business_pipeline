from django import forms
from django.forms import inlineformset_factory

from .models import Product, PTFileEntry
from apps.department.models import Brand, Department, Color


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["department", "category", "subcategory", "brand", "article_number"]
        widgets = {
            "department": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "subcategory": forms.TextInput(attrs={"class": "form-control"}),
            "brand": forms.TextInput(attrs={"class": "form-control"}),
            "article_number": forms.TextInput(attrs={"class": "form-control"}),
        }


class UploadFileForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"class": "form-control my-4"})
    )


class BrandSelectionForm(forms.Form):
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        empty_label="Select a Brand",
        widget=forms.Select(attrs={"class": "form-control select2"}),
    )


class ManualFeedingForm(forms.Form):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        widget=forms.Select(attrs={"class": "form-control select2"}),
    )
    article = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={
                "class": "form-control article-autocomplete",
                "placeholder": "Enter Article Number",
                "autocomplete": "off",
                "data-autocomplete": "true",
            }
        ),
    )
    color = forms.ModelChoiceField(
        queryset=Color.objects.all(),
        empty_label="Select Color",
        widget=forms.Select(attrs={"class": "form-control select2"}),
    )
    number_of_rows = forms.IntegerField(
        min_value=1,
        max_value=100,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Enter number of rows"}
        ),
    )
    photo_data = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,  # We'll validate this manually
    )

    def clean_photo_data(self):
        photo_data = self.cleaned_data.get("photo_data")
        if not photo_data:
            raise forms.ValidationError(
                "Photo is required. Please capture a photo before submitting."
            )

        if not photo_data.startswith("data:image/"):
            raise forms.ValidationError(
                "Invalid image format. Please capture a new photo."
            )

        return photo_data
