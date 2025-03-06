from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=200, required=True)
    password = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput())
    email = forms.EmailField(required=True)

