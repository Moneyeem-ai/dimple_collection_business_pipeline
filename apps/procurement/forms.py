from django import forms
from .models import ProcurementOrder


class ProcurementOrderForm(forms.ModelForm):
    class Meta:
        model = ProcurementOrder
        fields = "__all__"
