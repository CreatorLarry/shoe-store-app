from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class VendorRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
