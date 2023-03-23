from django import forms
from .models import Shopper


class UserForm(forms.ModelForm):
    # pour le mot de passe on modifie le widget
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Shopper
        fields = ["first_name", "last_name", "email", "password"]
