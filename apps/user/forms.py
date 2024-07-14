from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.user.models import UserType,User


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
                }
            ),
        required=True
        )
    user_type = forms.ChoiceField(
        choices=UserType.choices,
        widget=forms.Select(
            attrs={
                'class': 'form-control', 
                'id': 'group-select'
                }
            ),
        required=True
        )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
                }
            ),
            required=True
        )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
                }
            ),
            required=True
        )

    class Meta:
        model = User
        fields = ('email',  'user_type', 'password1', 'password2')