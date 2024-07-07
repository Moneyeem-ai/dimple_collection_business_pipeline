from django import forms
from .models import ProcurmentOrder


class ProcurmentOrderForm(forms.ModelForm):
    class Meta:
        model = ProcurmentOrder
        fields = "__all__"
