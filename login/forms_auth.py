import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users

class UsersLoginFrom(forms.Form):
    email = forms.EmailField(label='Email',required=True)
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(), required=True)

class UsersCreationFrom(UserCreationForm):
    class Meta:
        model = Users
        fields = ['email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }


