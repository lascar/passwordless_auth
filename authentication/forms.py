from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from .models import CustomUser
from django.utils.translation import gettext as _

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password-input'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    # Add an additional field for password strength
    password_strength = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
