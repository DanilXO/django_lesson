from django import forms
from django.contrib.auth.models import User


class LogInForm(forms.Form):
    username = forms.CharField(label='Login: ', max_length=100)
    password = forms.CharField(label='Password: ', widget=forms.PasswordInput())


class SignUpForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)